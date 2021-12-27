# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from .player import TTTPlayer, JBPlayer

class Action:
    def __init__(self, raw_line:str, timestamp:str):
        self.timestamp = list(map(int, timestamp.split(':')))
        self.raw_line = raw_line

class TTTAction(Action):
    def __init__(self, raw_line:str, timestamp:str, attacker:TTTPlayer=None, victim:TTTPlayer=None, weapon:str=None):
        super().__init__(raw_line, timestamp)
        self.attacker = attacker
        self.victim = victim
        self.weapon = weapon
        self.bad = raw_line.endswith(' - BAD ACTION')

    def involves_player(self, player):
        if isinstance(player, str):
            return self.attacker.name == player or self.victim.name == player
        elif isinstance(player, TTTPlayer):
            return self.attacker == player or self.victim == player
        else:
            raise ValueError('Player needs to be either str or TTTPlayer')

    def is_victim(self, player):
        if isinstance(player, str):
            return self.victim.name == player
        elif isinstance(player, TTTPlayer):
            return self.victim == player
        else:
            raise ValueError('Player needs to be either str or TTTPlayer')

    def is_attacker(self, player):
        if isinstance(player, str):
            return self.attacker.name == player
        elif isinstance(player, TTTPlayer):
            return self.attacker == player
        else:
            raise ValueError('Player needs to be either str or TTTPlayer')

    def using_weapon(self, weapon):
        return self.weapon.casefold() == weapon.casefold()

    def __str__(self):
        return self.raw_line

    def __repr__(self):
        return self.__str__()

class JBAction(Action):
    def __init__(self, raw_line:str, timestamp:str):
        super().__init__(raw_line, timestamp)

class TTTDamage(TTTAction):
    def __init__(self, raw_line:str, timestamp:str, attacker:TTTPlayer, victim:TTTPlayer, dmg:int, weapon:str):
        super().__init__(raw_line, timestamp, attacker, victim, weapon)
        self.damage = dmg

class TTTDeath(TTTAction):
    def __init__(self, raw_line:str, timestamp:str, attacker:TTTPlayer, victim:TTTPlayer, weapon:str):
        super().__init__(raw_line, timestamp, attacker, victim, weapon)
