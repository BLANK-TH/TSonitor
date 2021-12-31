# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import re

from .file import load_constants

constants = load_constants()
VERSION = '1.0.1'

TTT_ROUND_REGEX = re.compile(constants["ttt"]["regex"]["round"])
TTT_TIME_REGEX = re.compile(constants["ttt"]["regex"]["time"])
TTT_DAMAGE_REGEX = re.compile(constants["ttt"]["regex"]["damage"])
TTT_KILL_REGEX = re.compile(constants["ttt"]["regex"]["kill"])

STATUS_REGEX = re.compile(constants["age"]["regex"])

JB_DEATH_REGEX = re.compile(constants["jb"]["regex"]["death"])
JB_DAMAGE_REGEX = re.compile(constants["jb"]["regex"]["damage"])
JB_BUTTON_REGEX = re.compile(constants["jb"]["regex"]["button"])
JB_VENT_WALL_REGEX = re.compile(constants["jb"]["regex"]["ventwall"])
JB_UTILITY_REGEX = re.compile(constants["jb"]["regex"]["utility"])
JB_WARDEN_DEATH_REGEX = re.compile(constants["jb"]["regex"]["wardendeath"])
JB_NEW_WARDEN_REGEX = re.compile(constants["jb"]["regex"]["newwarden"])
JB_PASS_FIRE_REGEX = re.compile(constants["jb"]["regex"]["passfire"])
JB_WEAPON_DROP_REGEX = re.compile(constants["jb"]["regex"]["weapondrop"])
JB_TIME_REGEX = re.compile(constants["jb"]["regex"]["time"])
