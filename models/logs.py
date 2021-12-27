# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from .actions import TTTDeath, TTTDamage

class Log:
    def __init__(self, raw_log:str, actions:list, id:int, ty:str='Unknown'):
        self.raw_log = ""
        for line in raw_log.split('\n'):
            if line.startswith('[') and not line.startswith('[DS]'):
                self.raw_log += line + '\n'
        self.actions = actions
        self.id = id
        self.type = ty

    def save_log(self):
        with open('data/logs/{}_{}.txt'.format(self.type, id), 'r') as f:
            f.write(self.raw_log)

    def __str__(self):
        return self.raw_log

    def __repr__(self):
        return self.__str__()

class TTTLog(Log):
    def __init__(self, raw_log:str, actions:list, id:int):
        super().__init__(raw_log, actions, id, 'TTT')

    def summary_output(self, kills: bool, damage: bool):
        output = ""
        for action in self.actions:
            if kills and isinstance(action, TTTDeath):
                output += '[{}:{}] {} killed {}\n'.format(*action.timestamp, repr(action.attacker), repr(action.victim))
            elif damage and isinstance(action, TTTDamage):
                output += '[{}:{}] {} damaged {} for {:,}\n'.format(*action.timestamp, repr(action.attacker),
                                                                    repr(action.victim), action.damage)

        return output.rstrip()

class JBLog(Log):
    def __init__(self, raw_log:str, actions:list, id:int):
        super().__init__(raw_log, actions, id, 'JB')
