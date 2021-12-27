# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import re

from .file import load_constants

constants = load_constants()

TTT_ROUND_REGEX = re.compile(constants["ttt"]["regex"]["round"])
TTT_TIME_REGEX = re.compile(constants["ttt"]["regex"]["time"])
TTT_DAMAGE_REGEX = re.compile(constants["ttt"]["regex"]["damage"])
TTT_KILL_REGEX = re.compile(constants["ttt"]["regex"]["kill"])

STATUS_REGEX = re.compile(constants["age"]["regex"])
