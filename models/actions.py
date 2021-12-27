# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from .player import TTTPlayer, JBPlayer

class Action:
    """Class representing all actions in JB & TTT logs"""
    def __init__(self, raw_line:str, timestamp:str):
        self.timestamp = list(map(int, timestamp.split(':')))
        self.raw_line = raw_line

    def __str__(self):
        return self.raw_line

    def __repr__(self):
        return self.__str__()

class TTTAction(Action):
    """Class representing actions in TTT logs"""
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

class JBAction(Action):
    """Class representing actions in JB logs"""
    def __init__(self, raw_line:str, timestamp:str):
        super().__init__(raw_line, timestamp)

class TTTDamage(TTTAction):
    """Class representing damage in TTT logs"""
    def __init__(self, raw_line:str, timestamp:str, attacker:TTTPlayer, victim:TTTPlayer, dmg:int, weapon:str):
        super().__init__(raw_line, timestamp, attacker, victim, weapon)
        self.damage = dmg

class TTTDeath(TTTAction):
    """Class representing a death in TTT logs"""
    def __init__(self, raw_line:str, timestamp:str, attacker:TTTPlayer, victim:TTTPlayer, weapon:str):
        super().__init__(raw_line, timestamp, attacker, victim, weapon)

class JBWarden(JBAction):
    """Class representing someone becoming warden in JB logs"""
    def __init__(self, raw_line:str, timestamp:str, warden:JBPlayer):
        super().__init__(raw_line, timestamp)
        self.warden = warden

class JBVents(JBAction):
    """Class representing someone breaking a wall or vent in JB logs"""
    def __init__(self, raw_line:str, timestamp:str, player:JBPlayer):
        super().__init__(raw_line, timestamp)
        self.player = player

class JBButton(JBAction):
    """Class representing someone pressing a button in JB logs"""
    def __init__(self, raw_line:str, timestamp:str, player:JBPlayer, button_id:str):
        super().__init__(raw_line, timestamp)
        self.player = player
        self.button_id = button_id

class JBUtility(JBAction):
    """Class representing someone throwing utility in JB logs"""
    def __init__(self, raw_line:str, timestamp:str, player:JBPlayer, t:str):
        super().__init__(raw_line, timestamp)
        self.player = player
        self.type = t

class JBDamage(JBAction):
    """Class representing someone being damaged in JB logs"""
    def __init__(self, raw_line:str, timestamp:str, attacker:JBPlayer, victim:JBPlayer, dmg:int, weapon:str):
        super().__init__(raw_line, timestamp)
        self.attacker = attacker
        self.victim = victim
        self.damage = dmg
        self.weapon = weapon

class JBDeath(JBAction):
    """Class representing someone dying in JB logs"""
    def __init__(self, raw_line:str, timestamp:str, attacker:JBPlayer, victim:JBPlayer, weapon:str):
        super().__init__(raw_line, timestamp)
        self.attacker = attacker
        self.victim = victim
        self.weapon = weapon

class JBWardenDeath(JBAction):
    """Class representing warden dying in JB logs"""
    def __init__(self, raw_line:str, timestamp:str, warden:JBPlayer):
        super().__init__(raw_line, timestamp)
        self.warden = warden

class JBWeaponDrop(JBAction):
    """Class representing a weapon being dropped in JB logs"""
    def __init__(self, raw_line:str, timestamp:str, player:JBPlayer, weapon:str):
        super().__init__(raw_line, timestamp)
        self.player = player
        self.weapon = weapon

class JBWardenPassFire(JBAction):
    """Class representing a warden passing (manually or through disconnect) or being fired"""
    def __init__(self, raw_line:str, timestamp:str, warden:JBPlayer):
        super().__init__(raw_line, timestamp)
        self.warden = warden
