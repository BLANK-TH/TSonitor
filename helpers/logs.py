# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from time import time

import human_readable
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
    suppressable = ['days', 'hours', 'minutes', 'seconds']
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


def get_jb_player(players: dict, name: str, role: str):
    if name not in players:
        if role == 'Rebel':
            role = 'Prisoner'
        elif role == 'Warden':
            role = 'Guard'
        players[name] = JBPlayer(name, role)
    return players[name]


def parse_ttt_logs(lines: list) -> TTTLog:
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
            attacker = rd.group('attacker')
            victim = rd.group('victim')
            if attacker not in players:
                players[attacker] = TTTPlayer(attacker, rd.group('attacker_role'))
            if victim not in players:
                players[victim] = TTTPlayer(victim, rd.group('victim_role'))
            attacker = players[attacker]
            victim = players[victim]
            actions.append(TTTDamage(line, rd.group('time'), attacker, victim, int(rd.group('damage')),
                                     rd.group('weapon')))
            continue

        rk = handle_named_regex(TTT_KILL_REGEX, line)
        if rk is not None:
            attacker = rk.group('attacker')
            victim = rk.group('victim')
            if attacker not in players:
                players[attacker] = TTTPlayer(attacker, rk.group('attacker_role'))
            if victim not in players:
                players[victim] = TTTPlayer(victim, rk.group('victim_role'))
            attacker = players[attacker]
            victim = players[victim]
            actions.append(TTTDeath(line, rk.group('time'), attacker, victim, rk.group('weapon')))

        r = TTT_TIME_REGEX.findall(line)
        if r is not None and len(r) > 0:
            actions.append(TTTAction(line, r[0]))

    if round_number is None:
        raise ValueError('Round number could not be found, log may be incomplete:\n' + '\n'.join(lines))

    return TTTLog('\n'.join(lines), actions, round_number)


def parse_jb_logs(lines: list, round_number: int) -> JBLog:
    actions = []
    players = {'The World': JBWorld()}
    for line in lines:
        line = line.strip()

        r = handle_named_regex(JB_DEATH_REGEX, line)
        if r is not None:
            victim = get_jb_player(players, r.group('victim'), r.group('victim_role'))
            if victim.death_delta is None:
                # Only add to actions if victim is not already dead, repeated deaths happen with ghosts
                attacker = get_jb_player(players, r.group('attacker'), r.group('attacker_role'))
                actions.append(JBDeath(line, r.group('time'), attacker, victim))
                attacker.add_action(actions[-1], r.group('attacker_role'))
                victim.add_action(actions[-1], r.group('victim_role'))
            continue

        r = handle_named_regex(JB_DAMAGE_REGEX, line)
        if r is not None:
            attacker = get_jb_player(players, r.group('attacker'), r.group('attacker_role'))
            victim = get_jb_player(players, r.group('victim'), r.group('victim_role'))
            actions.append(JBDamage(line, r.group('time'), attacker, victim, int(r.group('damage')), r.group('weapon')))
            attacker.add_action(actions[-1], r.group('attacker_role'))
            victim.add_action(actions[-1], r.group('victim_role'))
            continue

        r = handle_named_regex(JB_BUTTON_REGEX, line)
        if r is not None:
            player = get_jb_player(players, r.group('player'), r.group('player_role'))
            actions.append(JBButton(line, r.group('time'), player, r.group('button_name'),
                                    int(r.group('button_number')) if r.group('button_number') is not None else None))
            player.add_action(actions[-1], r.group('player_role'))
            continue

        r = handle_named_regex(JB_VENT_WALL_REGEX, line)
        if r is not None:
            player = get_jb_player(players, r.group('player'), r.group('player_role'))
            actions.append(JBVents(line, r.group('time'), player))
            player.add_action(actions[-1], r.group('player_role'))
            continue

        r = handle_named_regex(JB_UTILITY_REGEX, line)
        if r is not None:
            player = get_jb_player(players, r.group('player'), r.group('player_role'))
            actions.append(JBUtility(line, r.group('time'), player, r.group('type')))
            player.add_action(actions[-1], r.group('player_role'))
            continue

        r = handle_named_regex(JB_WARDEN_DEATH_REGEX, line)
        if r is not None:
            player = get_jb_player(players, r.group('player'), 'Warden')
            actions.append(JBWardenDeath(line, r.group('time'), player))
            player.add_action(actions[-1], 'Warden')
            continue

        r = handle_named_regex(JB_NEW_WARDEN_REGEX, line)
        if r is not None:
            player = get_jb_player(players, r.group('player'), 'Warden')
            actions.append(JBWarden(line, r.group('time'), player))
            player.add_action(actions[-1], 'Warden')
            continue

        r = handle_named_regex(JB_PASS_FIRE_REGEX, line)
        if r is not None:
            player = get_jb_player(players, r.group('player'), 'Warden')
            actions.append(JBWardenPassFire(line, r.group('time'), player))
            player.add_action(actions[-1], 'Warden')
            continue

        r = handle_named_regex(JB_WEAPON_DROP_REGEX, line)
        if r is not None:
            player = get_jb_player(players, r.group('player'), r.group('player_role'))
            actions.append(JBWeaponDrop(line, r.group('time'), player, r.group('weapon')))
            player.add_action(actions[-1], r.group('player_role'))
            continue

        r = handle_named_regex(JB_TIME_REGEX, line)
        if r is not None:
            actions.append(JBAction(line, r.group('time')))

    return JBLog('\n'.join(lines), actions, round_number, [i for i in players.values() if not isinstance(i, JBWorld)])


def parse_status(steamapi, line, regex, cache, check_private, max_guess_iterations, check_csgo_playtime):
    if steamapi is None:
        raise ValueError('Steam API key not provided')
    r = handle_named_regex(regex, line)
    if r is None:
        raise ValueError('Invalid line')
    approximate = False
    created = None
    steam_id = r.group('steam_id')
    uuid = SteamID(steam_id).as_64
    if steam_id not in cache:
        try:
            p = steamapi.call('ISteamUser.GetPlayerSummaries', steamids=uuid)['response']['players']
            if len(p) == 0:
                raise ValueError('Invalid steam ID')
            created = p[0]['timecreated']
        except KeyError:
            if check_private:
                approximate = True
                iterations = 0
                while created is None:
                    if iterations > max_guess_iterations:
                        return float('inf'), r.group('user_id'), r.group('name'), 'Max guess iterations reached', \
                               False, None
                    uuid += 1
                    iterations += 1
                    p = steamapi.call('ISteamUser.GetPlayerSummaries', steamids=uuid)['response']['players']
                    if len(p) == 0:
                        continue
                    try:
                        created = p[0]['timecreated']
                    except KeyError:
                        continue
            else:
                return float('inf'), r.group('user_id'), r.group('name'), 'Guessing disabled', False, None
        cache[steam_id] = created, approximate
    else:
        created, approximate = cache[steam_id]

    td = timedelta(seconds=time() - created)
    td2 = None

    if check_csgo_playtime and not approximate:
        try:
            p = steamapi.call('ISteamUserStats.GetUserStatsForGame', steamid=uuid, appid=730)
        except HTTPError:
            pass
        else:
            td2 = timedelta(seconds=next((i for i in p['playerstats']['stats'] if i['name'] == 'total_time_played'),
                                         None)['value'])

    return created, r.group('user_id'), r.group('name'), human_readable.precise_delta(
        td, suppress=find_human_suppress(td)), approximate, human_readable.precise_delta(
        td2, suppress=find_human_suppress(td2)) if td2 is not None else None
