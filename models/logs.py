# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from collections import defaultdict
from typing import Union, Tuple, List

from .actions import *
from .player import JBWorld


def delta_range(td1: timedelta, td2: timedelta, minutes: int = 0, seconds: int = 0) -> bool:
    return abs(td1 - td2) <= timedelta(minutes=minutes, seconds=seconds)


class Log:
    """General class representing eGO logs"""

    def __init__(self, raw_log: str, actions: list, id: int, ty: str = 'Unknown'):
        self.raw_log = ""
        for line in raw_log.split('\n'):
            if line.startswith('[') and not line.startswith('[DS]'):
                self.raw_log += line + '\n'
        self.actions = actions
        self.id = id
        self.type = ty

    def save_log(self):
        with open('data/logs/{}_{}.txt'.format(self.type, self.id), 'w', encoding='utf-8') as f:
            try:
                f.write(self.raw_log)
            except UnicodeEncodeError:
                print("Failed to encode Log #" + str(self.id))

    def __str__(self):
        return self.raw_log

    def __repr__(self):
        return self.__str__()


class TTTLog(Log):
    """Class representing TTT logs"""

    def __init__(self, raw_log: str, actions: list, id: int):
        super().__init__(raw_log, actions, id, 'TTT')

    def summary_output(self, kills: bool, damage: bool):
        output = ""
        for action in self.actions:
            if kills and isinstance(action, TTTDeath):
                output += '[{:02}:{:02}] {} killed {}\n'.format(*action.timestamp, repr(action.attacker),
                                                                repr(action.victim))
            elif damage and isinstance(action, TTTDamage):
                output += '[{:02}:{:02}] {} damaged {} for {:,}\n'.format(*action.timestamp, repr(action.attacker),
                                                                          repr(action.victim), action.damage)

        return output.rstrip()

    def find_rdm(self, detect_reason: bool):
        rdms = []
        for i, action in enumerate(self.actions):
            if action.bad and isinstance(action, TTTDeath):
                if detect_reason:
                    for a in self.actions[:i]:
                        if (isinstance(action, TTTDamage) or isinstance(action, TTTDeath)) and a.is_victim(
                                action.attacker) and a.is_attacker(action.victim) and a.bad:
                            break
                    else:
                        rdms.append(action)
                else:
                    rdms.append(action)

        return rdms

    def find_mass_rdm(self, limit: int, detect_reason: bool):
        rdm_count = defaultdict(lambda: 0)
        for i, action in enumerate(self.actions):
            if action.bad and isinstance(action, TTTDeath):
                if detect_reason:
                    for a in self.actions[:i]:
                        if (isinstance(action, TTTDamage) or isinstance(action, TTTDeath)) and a.is_victim(
                                action.attacker) and a.is_attacker(action.victim) and a.bad:
                            break
                    else:
                        rdm_count[action.attacker] += 1
                else:
                    rdm_count[action.attacker] += 1

        return {player: amount for player, amount in rdm_count.items() if amount >= limit}

    def find_innocent_utility(self, utility_weapon_names, bad_only):
        damage_count = defaultdict(lambda: {'Innocent': [], 'Detective': [], 'Traitor': [], 'damage': 0})
        for action in self.actions:
            if isinstance(action, TTTDamage) and action.attacker.role in ['Innocent', 'Detective']:
                if action.weapon not in utility_weapon_names:
                    continue
                if not action.bad and bad_only:
                    continue
                damage_count[action.attacker][action.victim.role].append(action.victim)
                damage_count[action.attacker]['damage'] += action.damage

        return {k: [len(set(v['Innocent'])), len(set(v['Detective'])), len(set(v['Traitor'])), v['damage']]
                for k, v in damage_count.items()}


class JBLog(Log):
    """Class representing JB logs"""

    def __init__(self, raw_log: str, actions: list, id: int, players: List[JBPlayer]):
        super().__init__(raw_log, actions, id, 'JB')
        self.players = players
        self.deaths = [action for action in self.actions if isinstance(action, JBDeath)]
        self.ts = []
        self.cts = []
        self.t_deaths = []
        self.ct_deaths = []
        self.ct_win = self.deaths[-1].attacker.is_ct()
        for player in self.players:
            if player.is_t():
                self.ts.append(player)
            elif player.is_ct():
                self.cts.append(player)
        for death in self.deaths:
            if death.victim.is_t():
                self.t_deaths.append(death)
            elif death.victim.is_ct():
                self.ct_deaths.append(death)

        self.last_guard, self.last_request = self.get_lr_lg()

    def summary_output(self, kills: bool, warden: bool, warden_death: bool, pass_fire: bool, damage: bool, vents: bool,
                       button: bool, drop_weapon: bool) -> str:
        output = []
        for action in self.actions:
            if (kills and isinstance(action, JBDeath)) or (warden and isinstance(action, JBWarden)) or \
                    (warden_death and isinstance(action, JBWardenDeath)) or \
                    (pass_fire and isinstance(action, JBWardenPassFire)) or \
                    (damage and isinstance(action, JBDamage)) or (vents and isinstance(action, JBVents)) or \
                    (vents and isinstance(action, JBVents)) or (button and isinstance(action, JBButton)) or \
                    (drop_weapon and isinstance(action, JBWeaponDrop)):
                output.append(repr(action))

        if self.last_guard is not None and (self.last_request is None or
                                            self.last_request.timestamp_delta > self.last_guard.timestamp_delta):
            output.append('{} died, activating last guard at {:02}:{:02}'.format(self.last_guard.victim.name,
                                                                                 *self.last_guard.timestamp))
        if self.last_request is not None:
            output.append('{} died, activating last request at {:02}:{:02}'.format(self.last_request.victim.name,
                                                                                   *self.last_request.timestamp))

        return '\n'.join(output)

    def find_wardenless_fk(self, freeday_delay: int) -> List[JBDeath]:
        warden = False
        fks = []
        for action in self.actions:
            if isinstance(warden, timedelta):
                if abs(warden - action.timestamp_delta) > timedelta(seconds=freeday_delay):
                    warden = False
            if isinstance(action, JBWarden):
                warden = True
            elif isinstance(action, JBWardenDeath):
                warden = False
            elif isinstance(action, JBWardenPassFire):
                warden = action.timestamp_delta
            elif not warden and isinstance(action, JBDeath) and action.attacker.is_ct() and action.victim.is_inno(
                    action) and not (
                    self.last_guard is not None and action.timestamp_delta >= self.last_guard.timestamp_delta):
                fks.append(action)

        return fks

    def find_new_warden_fk(self, seconds_limit: int) -> List[JBDeath]:
        new_warden = None
        fks = []
        for action in self.actions:
            if isinstance(action, JBWarden):
                new_warden = action.timestamp_delta
            elif new_warden is not None and isinstance(action, JBDeath):
                if delta_range(action.timestamp_delta, new_warden, seconds=seconds_limit):
                    if action.attacker.is_ct() and action.victim.is_inno(action):
                        fks.append(action)
                else:
                    new_warden = None

        return fks

    def find_early_vent(self) -> List[JBVents]:
        players = []
        for action in self.actions:
            if isinstance(action, JBVents):
                if action.player.is_ct():
                    players.append(action.player)
                elif action.player.is_t():
                    break

        return players

    def find_gunplant(self, gunplant_delay: int) -> List[dict]:
        check_gunplants = []
        gunplants = []
        for action in self.actions:
            if isinstance(action, JBWeaponDrop) and action.player.is_ct():
                if action.player.death_delta is not None and action.timestamp_delta >= action.player.death_delta:
                    continue  # Skip gunplants caused by CT's death
                check_gunplants.append({'weapon': action.weapon, 'delta': action.timestamp_delta,
                                        'player': action.player})
            elif isinstance(action, JBDamage) and action.attacker.is_t():
                pending_remove = []
                for plant in [i for i in check_gunplants if i['weapon'] == action.weapon]:
                    if delta_range(plant['delta'], action.timestamp_delta, seconds=gunplant_delay):
                        gunplants.append({'ct': plant['player'], 't': action.attacker, 'weapon': action.weapon})
                    else:
                        pending_remove.append(plant)
                for remove in pending_remove:
                    check_gunplants.remove(remove)

        return gunplants

    def find_button(self, delay: int, threshold: int, ignore_warden: bool) -> dict:
        check_buttons = []
        griefs = defaultdict(lambda: {'prisoner': [], 'guard': []})
        for action in self.actions:
            if isinstance(action, JBButton) and not (ignore_warden and action.player.is_warden(action)):
                check_buttons.append(action)
            elif isinstance(action, JBDamage) and isinstance(action.attacker, JBWorld) and action.damage >= threshold:
                pending_remove = []
                for button in check_buttons:
                    if delta_range(button.timestamp_delta, action.timestamp_delta, seconds=delay):
                        griefs[button][action.victim.general_role.casefold()].append(action.victim)
                    else:
                        pending_remove.append(button)
                for remove in pending_remove:
                    check_buttons.remove(remove)

        return {k: {k2: len(set(v2)) for k2, v2 in v.items()} for k, v in griefs.items()}

    def find_utility(self, delay: int, threshold: int) -> dict:
        check_utility = []
        griefs = defaultdict(lambda: {'prisoner': [], 'guard': []})
        for action in self.actions:
            if isinstance(action, JBUtility):
                check_utility.append(action)
            elif isinstance(action, JBDamage) and isinstance(action.attacker, JBWorld) and action.damage >= threshold:
                pending_remove = []
                for util in check_utility:
                    if delta_range(util.timestamp_delta, action.timestamp_delta, seconds=delay):
                        griefs[util][action.victim.general_role.casefold()].append(action.victim)
                    else:
                        pending_remove.append(util)
                for remove in pending_remove:
                    check_utility.remove(remove)

        return {k: {k2: len(set(v2)) for k2, v2 in v.items()} for k, v in griefs.items()}

    def get_lr_lg(self) -> Tuple[Union[JBDeath, None], ...]:
        last_request = None
        last_guard = None
        if len(self.t_deaths) > 2 and len(self.ts) - len(self.t_deaths) <= 2:
            last_request = self.t_deaths[-2]
        if len(self.ct_deaths) > 2 and len(self.cts) - len(self.ct_deaths) <= 1:
            last_guard = self.ct_deaths[-1 if self.ct_win else -2]

        return last_guard, last_request
