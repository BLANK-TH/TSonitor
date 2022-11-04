# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from collections import defaultdict
from typing import Union, Tuple, List

from helpers.gvars import colourify
from .actions import *
from .player import JBWorld


def delta_range(
    td1: timedelta, td2: timedelta, minutes: int = 0, seconds: int = 0
) -> bool:
    return abs(td1 - td2) <= timedelta(minutes=minutes, seconds=seconds)


class Log:
    """General class representing eGO logs"""

    def __init__(
        self,
        raw_log: str,
        actions: list,
        id: int,
        ty: str = "Unknown",
        header: str = "",
        footer: str = "",
    ):
        self.raw_log = ""
        for line in raw_log.split("\n"):
            if line.startswith("[") and not line.startswith("[DS]"):
                self.raw_log += line + "\n"
        self.actions = actions
        self.id = id
        self.type = ty
        self.header = header + "\n" if header != "" else ""
        self.footer = footer + "\n" if header != "" else ""

    def save_log(self, DATA_PATH: str):
        with open(
            DATA_PATH + "/logs/{}_{}.txt".format(self.type, self.id), "w", encoding="utf-8"
        ) as f:
            try:
                f.write(self.header + self.raw_log + self.footer)
            except UnicodeEncodeError:
                print("Failed to encode Log #" + str(self.id))

    def __str__(self):
        return self.raw_log

    def __repr__(self):
        return self.__str__()


class TTTLog(Log):
    """Class representing TTT logs"""

    def __init__(
        self, raw_log: str, actions: list, id: int, header: str = "", footer: str = ""
    ):
        super().__init__(raw_log, actions, id, "TTT", header, footer)

    def summary_output(self, kills: bool, damage: bool):
        output = ""
        for action in self.actions:
            if kills and isinstance(action, TTTDeath):
                output += "[{}] {} killed {}\n".format(
                    colourify("time", "{:02}:{:02}".format(*action.timestamp)),
                    repr(action.attacker),
                    repr(action.victim),
                )
            elif damage and isinstance(action, TTTDamage):
                output += "[{}] {} damaged {} for {}\n".format(
                    colourify("time", "{:02}:{:02}".format(*action.timestamp)),
                    repr(action.attacker),
                    repr(action.victim),
                    colourify("damage", ":,".format(action.damage)),
                )

        return output.rstrip()

    def find_rdm(self, detect_reason: bool):
        rdms = []
        for i, action in enumerate(self.actions):
            if action.bad and isinstance(action, TTTDeath):
                rdm = True
                if detect_reason:
                    rdm = False
                    for a in self.actions[:i]:
                        if isinstance(a, TTTDamage):
                            if (
                                a.is_attacker(action.attacker)
                                and a.is_victim(action.victim)
                                and a.bad
                            ):
                                rdm = True
                                break
                            if (
                                a.is_attacker(action.victim)
                                and a.is_victim(action.attacker)
                                and a.bad
                            ):
                                rdm = False
                                break
                if rdm:
                    rdms.append(action)

        return rdms

    def find_mass_rdm(self, limit: int, detect_reason: bool):
        rdm_count = defaultdict(lambda: 0)
        for i, action in enumerate(self.actions):
            if action.bad and isinstance(action, TTTDeath):
                rdm = True
                if detect_reason:
                    rdm = False
                    for a in self.actions[:i]:
                        if isinstance(a, TTTDamage):
                            if (
                                a.is_attacker(action.attacker)
                                and a.is_victim(action.victim)
                                and a.bad
                            ):
                                rdm = True
                                break
                            if (
                                a.is_attacker(action.victim)
                                and a.is_victim(action.attacker)
                                and a.bad
                            ):
                                rdm = False
                                break
                if rdm:
                    rdm_count[action.attacker] += 1

        return {
            player: amount for player, amount in rdm_count.items() if amount >= limit
        }

    def find_innocent_utility(self, utility_weapon_names, bad_only):
        damage_count = defaultdict(
            lambda: {"Innocent": [], "Detective": [], "Traitor": [], "damage": 0}
        )
        for action in self.actions:
            if isinstance(action, TTTDamage) and action.attacker.role in [
                "Innocent",
                "Detective",
            ]:
                if action.weapon not in utility_weapon_names:
                    continue
                if not action.bad and bad_only:
                    continue
                damage_count[action.attacker][action.victim.role].append(action.victim)
                damage_count[action.attacker]["damage"] += action.damage

        return {
            k: [
                len(set(v["Innocent"])),
                len(set(v["Detective"])),
                len(set(v["Traitor"])),
                v["damage"],
            ]
            for k, v in damage_count.items()
        }


class JBLog(Log):
    """Class representing JB logs"""

    def __init__(
        self,
        raw_log: str,
        actions: list,
        id: int,
        players: List[JBPlayer],
        header: str = "",
        footer: str = "",
    ):
        super().__init__(raw_log, actions, id, "JB", header, footer)
        self.players = players
        self.deaths = [action for action in self.actions if isinstance(action, JBDeath)]
        self.ts = []
        self.cts = []
        self.t_deaths = []
        self.ct_deaths = []
        self.ct_win = self.deaths[-1].attacker.is_ct() if len(self.deaths) > 0 else None
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

    def summary_output(
        self,
        kills: bool,
        warden: bool,
        warden_death: bool,
        pass_fire: bool,
        damage: bool,
        vents: bool,
        button: bool,
        drop_weapon: bool,
        pickup_weapon: bool,
        world: bool,
    ) -> str:
        output = []
        for action in self.actions:
            if (
                (kills and isinstance(action, JBDeath))
                or (warden and isinstance(action, JBWarden))
                or (warden_death and isinstance(action, JBWardenDeath))
                or (pass_fire and isinstance(action, JBWardenPassFire))
                or (damage and isinstance(action, JBDamage))
                or (vents and isinstance(action, JBVents))
                or (vents and isinstance(action, JBVents))
                or (button and isinstance(action, JBButton))
                or (drop_weapon and isinstance(action, JBWeaponDrop))
                or (pickup_weapon and isinstance(action, JBWeaponPickup))
            ):
                if not (
                    not world
                    and hasattr(action, "attacker")
                    and isinstance(action.attacker, JBWorld)
                ):
                    output.append(repr(action))

        if self.last_guard is not None and (
            self.last_request is None
            or self.last_request.timestamp_delta > self.last_guard.timestamp_delta
        ):
            output.append(
                "{} died, activating last guard at {}".format(
                    colourify("name", self.last_guard.victim.name),
                    colourify("time", "{:02}:{:02}".format(*self.last_guard.timestamp)),
                )
            )
        if self.last_request is not None:
            output.append(
                "{} died, activating last request at {}".format(
                    colourify("name", self.last_request.victim.name),
                    colourify(
                        "time", "{:02}:{:02}".format(*self.last_request.timestamp)
                    ),
                )
            )

        return "\n".join(output)

    def find_wardenless_fk(self, freeday_delay: int) -> List[JBDeath]:
        warden = False
        fks = []
        for action in self.actions:
            if isinstance(warden, timedelta):
                if abs(warden - action.timestamp_delta) > timedelta(
                    seconds=freeday_delay
                ):
                    warden = False
            if isinstance(action, JBWarden):
                warden = True
            elif isinstance(action, JBWardenDeath):
                warden = False
            elif isinstance(action, JBWardenPassFire):
                warden = action.timestamp_delta
            elif (
                not warden
                and isinstance(action, JBDeath)
                and action.attacker.is_ct()
                and action.victim.is_inno(action)
                and not self.is_lg_lr(action.timestamp_delta)
            ):
                fks.append(action)

        return fks

    def find_new_warden_fk(self, seconds_limit: int) -> List[JBDeath]:
        new_warden = None
        fks = []
        for action in self.actions:
            if isinstance(action, JBWarden):
                new_warden = action.timestamp_delta
            elif (
                new_warden is not None
                and isinstance(action, JBDeath)
                and not self.is_lg_lr(action.timestamp_delta)
            ):
                if delta_range(
                    action.timestamp_delta, new_warden, seconds=seconds_limit
                ):
                    if action.attacker.is_ct() and action.victim.is_inno(action):
                        fks.append(action)
                else:
                    new_warden = None

        return fks

    def find_st_kills(self) -> List[JBDeath]:
        fks = []
        for action in self.actions:
            if (
                isinstance(action, JBDeath)
                and action.victim.is_st(action)
                and action.attacker.is_ct()
            ):
                fks.append(action)
        return fks

    def find_early_vent(self) -> List[JBVents]:
        players = []
        last_action = None
        for action in self.actions:
            if isinstance(action, JBVents):
                if action.player.is_ct():
                    if not isinstance(last_action, JBButton):
                        players.append(action.player)
                elif action.player.is_t():
                    break
            last_action = action

        return players

    def find_gunplant(self, utility_names: list) -> List[dict]:
        gunplants = []
        for action in self.actions:
            if (
                isinstance(action, JBWeaponPickup)
                and action.picker.is_t()
                and action.dropper.is_ct()
                and action.weapon not in utility_names
            ):
                if (
                    action.dropper.death_delta is not None
                    and action.timestamp_delta >= action.dropper.death_delta
                ):
                    continue
                gunplants.append(
                    {"ct": action.dropper, "t": action.picker, "weapon": action.weapon}
                )

        return gunplants

    def find_button(self, delay: int, threshold: int, ignore_warden: bool) -> dict:
        check_buttons = []
        griefs = defaultdict(lambda: {"t": [], "ct": []})
        for action in self.actions:
            if (
                isinstance(action, JBButton)
                and not action.ignore
                and not (ignore_warden and action.player.is_warden(action))
            ):
                check_buttons.append(action)
            elif (
                isinstance(action, JBDamage)
                and isinstance(action.attacker, JBWorld)
                and action.damage >= threshold
            ):
                pending_remove = []
                for button in check_buttons:
                    if delta_range(
                        button.timestamp_delta, action.timestamp_delta, seconds=delay
                    ):
                        griefs[button][action.victim.general_role.casefold()].append(
                            action.victim
                        )
                    else:
                        pending_remove.append(button)
                for remove in pending_remove:
                    check_buttons.remove(remove)

        return {
            k: {k2: len(set(v2)) for k2, v2 in v.items()} for k, v in griefs.items()
        }

    def find_utility(self, delay: int, threshold: int) -> dict:
        check_utility = []
        griefs = defaultdict(lambda: {"t": [], "ct": []})
        for action in self.actions:
            if isinstance(action, JBUtility):
                check_utility.append(action)
            elif (
                isinstance(action, JBDamage)
                and isinstance(action.attacker, JBWorld)
                and action.damage >= threshold
            ):
                pending_remove = []
                for util in check_utility:
                    if delta_range(
                        util.timestamp_delta, action.timestamp_delta, seconds=delay
                    ):
                        griefs[util][action.victim.general_role.casefold()].append(
                            action.victim
                        )
                    else:
                        pending_remove.append(util)
                for remove in pending_remove:
                    check_utility.remove(remove)

        return {
            k: {k2: len(set(v2)) for k2, v2 in v.items()} for k, v in griefs.items()
        }

    def find_utility_mfd(self, duration: int, threshold: int, utility: dict) -> dict:
        check_utility = []
        mfds = defaultdict(lambda: [])
        for action in self.actions:
            if isinstance(action, JBUtility) and action.player.is_ct():
                check_utility.append(action)
            elif (
                isinstance(action, JBDamage)
                and action.weapon in utility.values()
                and not self.is_lg_lr(action.timestamp_delta)
            ):
                pending_remove = []
                for util in check_utility:
                    if delta_range(
                        util.timestamp_delta, action.timestamp_delta, seconds=duration
                    ):
                        try:
                            if (
                                action.attacker == util.player
                                and utility[util.type] == action.weapon
                            ):
                                mfds[util].append(action.victim)
                        except KeyError:
                            continue
                    else:
                        pending_remove.append(util)
                for remove in pending_remove:
                    check_utility.remove(remove)

        return {k: len(set(v)) for k, v in mfds.items() if len(set(v)) >= threshold}

    def get_lr_lg(self) -> Tuple[Union[JBDeath, None], ...]:
        last_request = None
        last_guard = None
        ts_left = len(self.ts) - len(self.t_deaths)
        if len(self.t_deaths) > 2 and ts_left <= 2:
            last_request = self.t_deaths[ts_left - 3]
        if len(self.ct_deaths) > 2 and len(self.cts) - len(self.ct_deaths) <= 1:
            last_guard = self.ct_deaths[-1 if self.ct_win else -2]

        return last_guard, last_request

    def is_lg_lr(self, delta):
        return (
            self.last_guard is not None and delta >= self.last_guard.timestamp_delta
        ) or (
            self.last_request is not None and delta >= self.last_request.timestamp_delta
        )
