# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from datetime import timedelta
from time import time

import human_readable
from steam.steamid import SteamID
from requests.exceptions import HTTPError

from helpers.gvars import TTT_ROUND_REGEX, TTT_TIME_REGEX, TTT_DAMAGE_REGEX, TTT_KILL_REGEX
from models.logs import TTTLog, JBLog
from models.actions import *

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

def parse_ttt_logs(lines:list) -> TTTLog:
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
        elif line.startswith('[') and not line.startswith('[DS]'):
            actions.append(TTTAction(line, TTT_TIME_REGEX.findall(line)[0]))

    if round_number is None:
        raise ValueError('Round number could not be found, log may be incomplete:\n' + '\n'.join(lines))

    return TTTLog('\n'.join(lines), actions, round_number)

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
            p = steamapi.call('ISteamUser.GetPlayerSummaries',steamids=uuid)['response']['players']
            if len(p) == 0:
                raise ValueError('Invalid steam ID')
            created = p[0]['timecreated']
        except KeyError:
            if check_private:
                approximate = True
                iterations = 0
                while created is None:
                    if iterations > max_guess_iterations:
                        return float('inf'), r.group('user_id'), r.group('name'), 'Max guess iterations reached',\
                               False, 'None'
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
                return float('inf'), r.group('user_id'), r.group('name'), 'Guessing disabled', False, 'None'
        cache[steam_id] = created, approximate
    else:
        created, approximate = cache[steam_id]

    td = timedelta(seconds=time()-created)
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
        td2, suppress=find_human_suppress(td2)) if td2 is not None else 'None'
