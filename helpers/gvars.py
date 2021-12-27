# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import re

from .file import load_constants

constants = load_constants()

TTT_ROUND_REGEX = re.compile(constants["ttt"]["round_regex"])
TTT_TIME_REGEX = re.compile(constants["ttt"]["time_regex"])
TTT_DAMAGE_REGEX = re.compile(constants["ttt"]["damage_regex"])
TTT_KILL_REGEX = re.compile(constants["ttt"]["kill_regex"])
