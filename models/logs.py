# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from collections import defaultdict

from .actions import *

class Log:
    """General class representing eGO logs"""
    def __init__(self, raw_log:str, actions:list, id:int, ty:str='Unknown'):
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
    def __init__(self, raw_log:str, actions:list, id:int):
        super().__init__(raw_log, actions, id, 'TTT')

    def summary_output(self, kills: bool, damage: bool):
        output = ""
        for action in self.actions:
            if kills and isinstance(action, TTTDeath):
                output += '[{:02}:{:02}] {} killed {}\n'.format(*action.timestamp, repr(action.attacker), repr(action.victim))
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

        return {player:amount for player, amount in rdm_count.items() if amount >= limit}

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

        return {k:[len(set(v['Innocent'])), len(set(v['Detective'])), len(set(v['Traitor'])), v['damage']]
                for k, v in damage_count.items()}

class JBLog(Log):
    """Class representing JB logs"""
    def __init__(self, raw_log:str, actions:list, id:int):
        super().__init__(raw_log, actions, id, 'JB')

    def summary_output(self, kills: bool, warden: bool, warden_death: bool, pass_fire: bool, damage: bool, vents: bool,
                       button: bool, drop_weapon: bool):
        output = []
        for action in self.actions:
            if (kills and isinstance(action, JBDeath)) or (warden and isinstance(action, JBWarden)) or \
                    (warden_death and isinstance(action, JBWardenDeath)) or \
                    (pass_fire and isinstance(action, JBWardenPassFire)) or \
                    (damage and isinstance(action, JBDamage)) or (vents and isinstance(action, JBVents)) or \
                    (vents and isinstance(action, JBVents)) or (button and isinstance(action, JBButton)) or \
                    (drop_weapon and isinstance(action, JBWeaponDrop)):
                output.append(repr(action))

        return '\n'.join(output)
