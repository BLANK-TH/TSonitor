# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

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
        self.role = role
