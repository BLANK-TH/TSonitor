# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

# noinspection PyUnresolvedReferences
import re
from time import time

import human_readable
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from steam.steamid import SteamID

from helpers.gvars import *
from models.actions import *
from models.logs import TTTLog, JBLog
from models.player import TTTPlayer, JBPlayer, JBWorld


def handle_named_regex(regex, search_string):
    try:
        return next(regex.finditer(search_string))
    except StopIteration:
        return None


def find_human_suppress(td: timedelta):
    suppressable = ["days", "hours", "minutes", "seconds"]
    if td.days >= 365:
        return suppressable
    elif td.days > 30:
        return suppressable[1:]
    elif td.days > 0:
        return suppressable[2:]
    elif td.seconds / 60 // 60 > 0:
        return suppressable[3:]
    else:
        return []


def get_playtime(steam_id: str, game_id: str, playerinfo: str) -> str:
    try:
        p = requests.get("{}/{}/{}".format(playerinfo, game_id, steam_id))
        if p.ok:
            return (
                [
                    i
                    for i in BeautifulSoup(p.content, "html.parser").select(
                        "div.container > div.cont_left > table.spacer_b > tr"
                    )
                    if i.find("td", text="Connection Time:") is not None
                ][0]
                .select("td[colspan]")[0]
                .text.replace("\xa0", " ")
            )
        else:
            return "Failed GET request with code " + str(p.status_code)
    except HTTPError as e:
        return "HTTPError: " + str(e)
    except IndexError:
        return "Not Found"


def get_jb_player(players: dict, name: str, role: str):
    if name not in players:
        if role in ["Prisoner", "Rebel", "ST"]:
            role = "T"
        elif role in ["Guard", "Warden"]:
            role = "CT"
        players[name] = JBPlayer(name, role)
    return players[name]


def parse_ttt_logs(lines: list, header: str = "", footer: str = "") -> TTTLog:
    actions = []
    players = {}
    round_number = None
    for line in lines:
        line = line.strip()
        rr = TTT_ROUND_REGEX.findall(line)
        if len(rr) == 1:
            round_number = int(rr[0])
            continue

        rd = handle_named_regex(TTT_DAMAGE_REGEX, line)
        if rd is not None:
            attacker = rd.group("attacker")
            victim = rd.group("victim")
            if attacker not in players:
                players[attacker] = TTTPlayer(attacker, rd.group("attacker_role"))
            if victim not in players:
                players[victim] = TTTPlayer(victim, rd.group("victim_role"))
            attacker = players[attacker]
            victim = players[victim]
            actions.append(
                TTTDamage(
                    line,
                    rd.group("time"),
                    attacker,
                    victim,
                    int(rd.group("damage")),
                    rd.group("weapon"),
                )
            )
            continue

        rk = handle_named_regex(TTT_KILL_REGEX, line)
        if rk is not None:
            attacker = rk.group("attacker")
            victim = rk.group("victim")
            if attacker not in players:
                players[attacker] = TTTPlayer(attacker, rk.group("attacker_role"))
            if victim not in players:
                players[victim] = TTTPlayer(victim, rk.group("victim_role"))
            attacker = players[attacker]
            victim = players[victim]
            actions.append(
                TTTDeath(line, rk.group("time"), attacker, victim, rk.group("weapon"))
            )

        r = TTT_TIME_REGEX.findall(line)
        if r is not None and len(r) > 0:
            actions.append(TTTAction(line, r[0]))

    if round_number is None:
        raise ValueError(
            "Round number could not be found, log may be incomplete:\n"
            + "\n".join(lines)
        )

    return TTTLog("\n".join(lines), actions, round_number, header, footer)


def parse_jb_logs(
    lines: list, round_number: int, buttons: dict, header: str = "", footer: str = ""
) -> JBLog:
    actions = []
    players = {"The World": JBWorld()}
    for line in lines:
        line = line.strip()

        r = handle_named_regex(JB_DEATH_REGEX, line)
        if r is not None:
            victim = get_jb_player(players, r.group("victim"), r.group("victim_role"))
            if victim.death_delta is None:
                # Only add to actions if victim is not already dead, repeated deaths happen with ghosts
                attacker = get_jb_player(
                    players, r.group("attacker"), r.group("attacker_role")
                )
                actions.append(JBDeath(line, r.group("time"), attacker, victim))
                attacker.add_action(actions[-1], r.group("attacker_role"))
                victim.add_action(actions[-1], r.group("victim_role"))
            continue

        r = handle_named_regex(JB_DAMAGE_REGEX, line)
        if r is not None:
            attacker = get_jb_player(
                players, r.group("attacker"), r.group("attacker_role")
            )
            victim = get_jb_player(players, r.group("victim"), r.group("victim_role"))
            actions.append(
                JBDamage(
                    line,
                    r.group("time"),
                    attacker,
                    victim,
                    int(r.group("damage")),
                    r.group("weapon"),
                )
            )
            attacker.add_action(actions[-1], r.group("attacker_role"))
            victim.add_action(actions[-1], r.group("victim_role"))
            continue

        r = handle_named_regex(JB_BUTTON_REGEX, line)
        if r is not None:
            player = get_jb_player(players, r.group("player"), r.group("player_role"))

            button_name = r.group("button_name")
            button_number = r.group("button_number")
            button_config = None
            ignore = False
            if button_name in buttons["normal"]:
                button_config = buttons["normal"][button_name]
            elif (
                isinstance(button_number, str)
                and "#" + button_number in buttons["normal"]
            ):
                button_config = buttons["normal"]["#" + button_number]
            else:
                for rg, v in buttons["regex"].items():
                    if re.fullmatch(rg, button_name):
                        button_config = v
                        break

            if button_config is not None:
                ignore = button_config["ignore"]
                if button_config["alias"] is not None:
                    button_name = button_config["alias"]

            actions.append(
                JBButton(
                    line,
                    r.group("time"),
                    player,
                    button_name,
                    int(button_number) if button_number is not None else None,
                    ignore,
                )
            )
            player.add_action(actions[-1], r.group("player_role"))
            continue

        r = handle_named_regex(JB_VENT_WALL_REGEX, line)
        if r is not None:
            player = get_jb_player(players, r.group("player"), r.group("player_role"))
            actions.append(JBVents(line, r.group("time"), player))
            player.add_action(actions[-1], r.group("player_role"))
            continue

        r = handle_named_regex(JB_UTILITY_REGEX, line)
        if r is not None:
            player = get_jb_player(players, r.group("player"), r.group("player_role"))
            actions.append(JBUtility(line, r.group("time"), player, r.group("type")))
            player.add_action(actions[-1], r.group("player_role"))
            continue

        r = handle_named_regex(JB_WARDEN_DEATH_REGEX, line)
        if r is not None:
            player = get_jb_player(players, r.group("player"), "Warden")
            actions.append(JBWardenDeath(line, r.group("time"), player))
            player.add_action(actions[-1], "Warden")
            continue

        r = handle_named_regex(JB_NEW_WARDEN_REGEX, line)
        if r is not None:
            player = get_jb_player(players, r.group("player"), "Warden")
            actions.append(JBWarden(line, r.group("time"), player))
            player.add_action(actions[-1], "Warden")
            continue

        r = handle_named_regex(JB_PASS_FIRE_REGEX, line)
        if r is not None:
            player = get_jb_player(players, r.group("player"), "Warden")
            actions.append(JBWardenPassFire(line, r.group("time"), player))
            player.add_action(actions[-1], "Warden")
            continue

        r = handle_named_regex(JB_WEAPON_DROP_REGEX, line)
        if r is not None:
            player = get_jb_player(players, r.group("player"), r.group("player_role"))
            actions.append(
                JBWeaponDrop(line, r.group("time"), player, r.group("weapon"))
            )
            player.add_action(actions[-1], r.group("player_role"))
            continue

        r = handle_named_regex(JB_WEAPON_PICKUP_REGEX, line)
        if r is not None:
            picker = get_jb_player(players, r.group("picker"), r.group("picker_role"))
            dropper = get_jb_player(
                players, r.group("dropper"), r.group("dropper_role")
            )
            actions.append(
                JBWeaponPickup(
                    line, r.group("time"), picker, dropper, r.group("weapon")
                )
            )
            picker.add_action(actions[-1], r.group("picker_role"))
            dropper.add_action(actions[-1], r.group("dropper_role"))
            continue

        r = handle_named_regex(JB_TIME_REGEX, line)
        if r is not None:
            actions.append(JBAction(line, r.group("time")))

    return JBLog(
        "\n".join(lines),
        actions,
        round_number,
        [i for i in players.values() if not isinstance(i, JBWorld)],
        header,
        footer,
    )


def parse_status(
    steamapi,
    line,
    regex,
    cache,
    check_private,
    max_guess_iterations,
    check_csgo_playtime,
    check_server_playtime,
    game_code_map,
    server_ip,
    playerinfo_url,
):
    if steamapi is None:
        raise ValueError("Steam API key not provided")
    r = handle_named_regex(regex, line)
    if r is None:
        raise ValueError("Invalid line, unable to parse")

    steam_id = r.group("steam_id")
    sid = SteamID(steam_id)
    uuid_working = sid.as_64

    r_created = None
    r_uid = r.group("user_id")
    r_name = r.group("name")
    r_age_td = None
    r_approximate = False
    r_lvl = None
    r_csplaytime_td = None
    r_server_playtime = None

    if steam_id not in cache:
        try:
            p = steamapi.call("ISteamUser.GetPlayerSummaries", steamids=uuid_working)[
                "response"
            ]["players"]
            if len(p) == 0:
                raise ValueError("Invalid Steam ID")
            r_created = p[0]["timecreated"]
        except KeyError:
            if check_private:
                r_approximate = True
                iterations = 0
                while r_created is None:
                    if iterations > max_guess_iterations:
                        r_age_td = "Max Guess Iterations Reached"
                        break
                    uuid_working += 1
                    iterations += 1
                    p = steamapi.call(
                        "ISteamUser.GetPlayerSummaries", steamids=uuid_working
                    )["response"]["players"]
                    if len(p) == 0:
                        continue
                    try:
                        r_created = p[0]["timecreated"]
                    except KeyError:
                        continue
            else:
                r_age_td = "Guessing Disabled"
        if not isinstance(r_age_td, str):
            cache[steam_id] = r_created, r_approximate
    else:
        r_created, r_approximate = cache[steam_id]

    if r_created is not None:
        r_age_td = timedelta(seconds=time() - r_created)

    if not r_approximate:
        try:
            p = steamapi.call("IPlayerService.GetSteamLevel", steamid=sid.as_64)
        except HTTPError:
            pass
        else:
            if "player_level" in p["response"]:
                r_lvl = p["response"]["player_level"]
        if check_csgo_playtime:
            try:
                p = steamapi.call(
                    "ISteamUserStats.GetUserStatsForGame", steamid=sid.as_64, appid=730
                )
            except HTTPError:
                pass
            else:
                r_csplaytime_td = timedelta(
                    seconds=next(
                        (
                            i
                            for i in p["playerstats"]["stats"]
                            if i["name"] == "total_time_played"
                        ),
                        None,
                    )["value"]
                )

    if check_server_playtime:
        try:
            r_server_playtime = get_playtime(
                sid.as_steam2_zero, game_code_map[server_ip], playerinfo_url
            )
        except KeyError:
            r_server_playtime = "Invalid Server"

    return (
        r_created if r_created is not None else float('inf'),
        r_uid,
        r_name,
        human_readable.precise_delta(r_age_td, suppress=find_human_suppress(r_age_td))
        if isinstance(r_age_td, timedelta)
        else r_age_td,
        r_approximate,
        r_lvl,
        human_readable.precise_delta(
            r_csplaytime_td, suppress=find_human_suppress(r_csplaytime_td)
        )
        if isinstance(r_csplaytime_td, timedelta)
        else r_csplaytime_td,
        r_server_playtime,
    )
