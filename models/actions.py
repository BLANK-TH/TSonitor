# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from datetime import timedelta
from typing import Union

from helpers.gvars import colourify, get_colour, RESET_COLOUR
from .player import TTTPlayer, JBPlayer


class Action:
    """Class representing all actions in JB & TTT logs"""

    def __init__(self, raw_line: str, timestamp: str):
        self.timestamp = list(map(int, timestamp.split(":")))
        self.timestamp_delta = timedelta(
            minutes=self.timestamp[0], seconds=self.timestamp[1]
        )
        self.raw_line = raw_line

    def __str__(self):
        return self.raw_line

    def __repr__(self):
        return self.__str__()


class TTTAction(Action):
    """Class representing actions in TTT logs"""

    def __init__(
        self,
        raw_line: str,
        timestamp: str,
        attacker: Union[TTTPlayer, str, None] = None,
        victim: Union[TTTPlayer, str, None] = None,
    ):
        super().__init__(raw_line, timestamp)
        self.attacker = attacker
        self.victim = victim
        self.bad = raw_line.endswith(" - BAD ACTION")

    def involves_player(self, player):
        if isinstance(player, str):
            return (
                getattr(self.attacker, "name", self.attacker) == player
                or getattr(self.victim, "name", self.victim) == player
            )
        elif isinstance(player, TTTPlayer):
            return self.attacker == (
                player if isinstance(self.attacker, TTTPlayer) else player.name
            ) or self.victim == (
                player if isinstance(self.victim, TTTPlayer) else player.name
            )
        raise ValueError("Unexpected type given for player")

    def is_victim(self, player):
        if isinstance(player, str):
            return getattr(self.victim, "name", self.victim) == player
        elif isinstance(player, TTTPlayer):
            return self.victim == (
                player if isinstance(self.victim, TTTPlayer) else player.name
            )
        else:
            raise ValueError("Player needs to be either str or TTTPlayer")

    def is_attacker(self, player):
        if isinstance(player, str):
            return getattr(self.attacker, "name", self.attacker) == player
        elif isinstance(player, TTTPlayer):
            return self.attacker == (
                player if isinstance(self.attacker, TTTPlayer) else player.name
            )
        else:
            raise ValueError("Player needs to be either str or TTTPlayer")


class JBAction(Action):
    """Class representing actions in JB logs"""

    def __init__(self, raw_line: str, timestamp: str):
        super().__init__(raw_line, timestamp)


class TTTDamage(TTTAction):
    """Class representing damage in TTT logs"""

    def __init__(
        self,
        raw_line: str,
        timestamp: str,
        attacker: TTTPlayer,
        victim: TTTPlayer,
        dmg: int,
        weapon: str,
    ):
        super().__init__(raw_line, timestamp, attacker, victim)
        self.weapon = weapon
        self.damage = dmg

    def using_weapon(self, weapon):
        return self.weapon.casefold() == weapon.casefold()

    def __repr__(self):
        return "[{}] {} damaged {} for {}".format(
            colourify("time", "{:02}:{:02}".format(*self.timestamp)),
            repr(self.attacker),
            repr(self.victim),
            colourify("damage", "{:,}".format(self.damage)),
        )


class TTTDeath(TTTAction):
    """Class representing a death in TTT logs"""

    def __init__(
        self,
        raw_line: str,
        timestamp: str,
        attacker: TTTPlayer,
        victim: TTTPlayer,
        weapon: str,
    ):
        super().__init__(raw_line, timestamp, attacker, victim)
        self.weapon = weapon

    def using_weapon(self, weapon):
        return self.weapon.casefold() == weapon.casefold()

    def __repr__(self):
        return "[{}] {} killed {}".format(
            colourify("time", "{:02}:{:02}".format(*self.timestamp)),
            repr(self.attacker),
            repr(self.victim),
        )


class TTTID(TTTAction):
    """Class representing a body being IDed in TTT logs"""

    def __init__(
        self, raw_line: str, timestamp: str, player: TTTPlayer, body: TTTPlayer
    ):
        super().__init__(raw_line, timestamp, player, body)
        self.player = self.attacker
        self.body = self.victim

    def __repr__(self):
        return "[{}] {} IDed {}'s body".format(
            colourify("time", "{:02}:{:02}".format(*self.timestamp)),
            repr(self.player),
            repr(self.body),
        )


class TTTDNAScan(TTTAction):
    """Class representing a body being DNA scanned by the Detective in TTT logs"""

    def __init__(
        self,
        raw_line: str,
        timestamp: str,
        player: TTTPlayer,
        killer: TTTPlayer,
        weapon: str,
    ):
        super().__init__(raw_line, timestamp, player, killer)
        self.player = self.attacker
        self.killer = self.victim
        self.weapon = weapon

    def __repr__(self):
        return "[{}] {} DNA scanned {} as the killer".format(
            colourify("time", "{:02}:{:02}".format(*self.timestamp)),
            repr(self.player),
            repr(self.killer),
        )


class TTTTase(TTTAction):
    """Class representing a taser being used on someone"""

    def __init__(
        self,
        raw_line: str,
        timestamp: str,
        attacker: Union[TTTPlayer, str],
        victim: TTTPlayer,
    ):
        super().__init__(raw_line, timestamp, attacker, victim)

    def __repr__(self):
        return "[{}] {} tased {}".format(
            colourify("time", "{:02}:{:02}".format(*self.timestamp)),
            repr(self.attacker)
            if isinstance(self.attacker, TTTPlayer)
            else f"{get_colour('name')}{self.attacker}{RESET_COLOUR}",
            repr(self.victim),
        )


class JBWarden(JBAction):
    """Class representing someone becoming warden in JB logs"""

    def __init__(self, raw_line: str, timestamp: str, warden: JBPlayer):
        super().__init__(raw_line, timestamp)
        self.warden = warden

    def __repr__(self):
        return "[{}] {} is now warden".format(
            colourify("time", "{:02}:{:02}".format(*self.timestamp)),
            colourify("name", self.warden.name),
        )


class JBVents(JBAction):
    """Class representing someone breaking a wall or vent in JB logs"""

    def __init__(self, raw_line: str, timestamp: str, player: JBPlayer):
        super().__init__(raw_line, timestamp)
        self.player = player

    def __repr__(self):
        return "[{}] {} broke a vent or wall".format(
            colourify("time", "{:02}:{:02}".format(*self.timestamp)),
            self.player.to_str(self),
        )


class JBButton(JBAction):
    """Class representing someone pressing a button in JB logs"""

    def __init__(
        self,
        raw_line: str,
        timestamp: str,
        player: JBPlayer,
        button_name: str,
        button_number: int = None,
        ignore: bool = False,
    ):
        super().__init__(raw_line, timestamp)
        self.player = player
        self.button_name = button_name
        self.button_number = button_number
        self.ignore = ignore

    def __repr__(self):
        return "[{}] {} pressed {}".format(
            colourify("time", "{:02}:{:02}".format(*self.timestamp)),
            self.player.to_str(self),
            colourify("button_name", self.button_str()),
        )

    def button_str(self):
        return self.button_name + (
            " (#{})".format(self.button_number)
            if self.button_number is not None
            else ""
        )


class JBUtility(JBAction):
    """Class representing someone throwing utility in JB logs"""

    def __init__(self, raw_line: str, timestamp: str, player: JBPlayer, t: str):
        super().__init__(raw_line, timestamp)
        self.player = player
        self.type = t

    def __repr__(self):
        return "[{}] {} threw a {}".format(
            colourify("time", "{:02}:{:02}".format(*self.timestamp)),
            self.player.to_str(self),
            colourify("weapon_name", self.type),
        )


class JBDamage(JBAction):
    """Class representing someone being damaged in JB logs"""

    def __init__(
        self,
        raw_line: str,
        timestamp: str,
        attacker: JBPlayer,
        victim: JBPlayer,
        dmg: int,
        weapon: str,
    ):
        super().__init__(raw_line, timestamp)
        self.attacker = attacker
        self.victim = victim
        self.damage = dmg
        self.weapon = weapon

    def __repr__(self):
        return "[{}] {} damaged {} for {} damage using {}".format(
            colourify("time", "{:02}:{:02}".format(*self.timestamp)),
            self.attacker.to_str(self),
            self.victim.to_str(self),
            colourify("damage", "{:,}".format(self.damage)),
            colourify("weapon_name", self.weapon),
        )


class JBDeath(JBAction):
    """Class representing someone dying in JB logs"""

    def __init__(
        self, raw_line: str, timestamp: str, attacker: JBPlayer, victim: JBPlayer
    ):
        super().__init__(raw_line, timestamp)
        self.attacker = attacker
        self.victim = victim

    def __repr__(self):
        return "[{}] {} killed {}".format(
            colourify("time", "{:02}:{:02}".format(*self.timestamp)),
            self.attacker.to_str(self),
            self.victim.to_str(self),
        )


class JBWardenDeath(JBAction):
    """Class representing warden dying in JB logs"""

    def __init__(self, raw_line: str, timestamp: str, warden: JBPlayer):
        super().__init__(raw_line, timestamp)
        self.warden = warden

    def __repr__(self):
        return "[{}] {} died and is no longer warden".format(
            colourify("time", "{:02}:{:02}".format(*self.timestamp)),
            colourify("name", self.warden.name),
        )


class JBWeaponDrop(JBAction):
    """Class representing a weapon being dropped in JB logs"""

    def __init__(self, raw_line: str, timestamp: str, player: JBPlayer, weapon: str):
        super().__init__(raw_line, timestamp)
        self.player = player
        self.weapon = weapon

    def __repr__(self):
        return "[{}] {} dropped weapon {}".format(
            colourify("time", "{:02}:{:02}".format(*self.timestamp)),
            self.player.to_str(self),
            colourify("weapon_name", self.weapon),
        )


class JBWeaponPickup(JBAction):
    """Class representing a weapon being picked up in JB logs"""

    def __init__(
        self,
        raw_line: str,
        timestamp: str,
        picker: JBPlayer,
        dropper: JBPlayer,
        weapon: str,
    ):
        super().__init__(raw_line, timestamp)
        self.picker = picker
        self.dropper = dropper
        self.weapon = weapon

    def __repr__(self):
        return "[{}] {} picked up {}'s {}".format(
            colourify("time", "{:02}:{:02}".format(*self.timestamp)),
            self.picker.to_str(self),
            self.dropper.to_str(self),
            colourify("weapon_name", self.weapon),
        )


class JBWardenPassFire(JBAction):
    """Class representing a warden passing (manually or through disconnect) or being fired"""

    def __init__(self, raw_line: str, timestamp: str, warden: JBPlayer):
        super().__init__(raw_line, timestamp)
        self.warden = warden

    def __repr__(self):
        return "[{}] {} has passed or was fired, and is no longer warden".format(
            colourify("time", "{:02}:{:02}".format(*self.timestamp)),
            colourify("name", self.warden.name),
        )
