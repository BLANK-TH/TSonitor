# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from collections import defaultdict

from helpers.gvars import config, colours, get_colour, RESET_COLOUR

colour_map = {
    "Traitor": colours["red"],
    "Detective": colours["blue"],
    "Innocent": colours["green"],
    "Prisoner": colours["yellow"],
    "Rebel": colours["red"],
    "Guard": colours["cyan"],
    "Warden": colours["blue"],
    "ST": colours["green"],
    "CT": colours["blue"],
    "T": colours["red"],
    None: colours["white"],
}


def get_colour_role(role):
    return (
        colour_map[role]
        if config["colours"]["enable"] and config["colours"]["role"] == "automatic"
        else get_colour("role")
    )


class TTTPlayer:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.bad_kills = 0
        self.role_colour = colour_map[role]

    def __str__(self):
        return get_colour_role(self.role) + self.name + RESET_COLOUR

    def __repr__(self):
        return f"{get_colour('name')}{self.name}{RESET_COLOUR} ({get_colour_role(self.role)}{self.role}{RESET_COLOUR})"


class JBPlayer:
    def __init__(self, name, role):
        self.name = name
        self.general_role = role
        self.context = defaultdict(lambda: self.general_role)
        self.death_delta = None

    def add_action(self, action, role):
        self.context[action] = role
        if (
            action.__class__.__name__ == "JBDeath"
        ):  # Manual comparison due to unavoidable circular import
            if action.victim == self:
                self.death_delta = action.timestamp_delta

    def __str__(self):
        return f"{get_colour('name')}{self.name}{RESET_COLOUR}"

    def __repr__(self):
        return f"{get_colour('name')}{self.name}{RESET_COLOUR} ({get_colour_role(self.general_role)}{self.general_role}{RESET_COLOUR})"

    def to_str(self, context=None):
        if context is None:
            return self.__str__()
        else:
            return f"{get_colour('name')}{self.name}{RESET_COLOUR} ({get_colour_role(self.get_role(context))}{self.get_role(context)}{RESET_COLOUR})"

    def get_role(self, context):
        return self.context[context]

    def is_ct(self):
        return self.general_role == "CT"

    def is_t(self):
        return self.general_role == "T"

    def is_inno(self, context):
        return self.context[context] in ["Prisoner", "ST"]

    def is_st(self, context):
        return self.context[context] == "ST"

    def is_warden(self, context):
        return self.context[context].casefold() == "warden"


class JBWorld(JBPlayer):
    def __init__(self):
        super().__init__("World", "World")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
