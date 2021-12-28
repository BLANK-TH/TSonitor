# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from collections import defaultdict

class TTTPlayer:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.bad_kills = 0

    def __str__(self):
        return self.name

    def __repr__(self):
        return '{} ({})'.format(self.name, self.role)

class JBPlayer:
    def __init__(self, name, role):
        self.name = name
        self.general_role = role
        self.context = defaultdict(lambda: self.general_role)

    def add_action(self, action, role):
        self.context[action] = role

    def __str__(self):
        return self.name

    def __repr__(self):
        return '{} ({})'.format(self.name, self.general_role)

    def to_str(self, context=None):
        if context is None:
            return self.__str__()
        else:
            return '{} ({})'.format(self.name, self.get_role(context))

    def get_role(self, context):
        return self.context[context]

    def is_ct(self):
        return self.general_role in ['Guard', 'Warden']

    def is_t(self):
        return self.general_role in ['Prisoner', 'Rebel']

    def is_inno(self, context):
        return self.context[context] == 'Prisoner'

    def is_warden(self, context):
        return self.context[context].casefold() == 'warden'

class JBWorld(JBPlayer):
    def __init__(self):
        super().__init__("World", "World")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
