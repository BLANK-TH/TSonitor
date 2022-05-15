# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import re

from colorama import Fore

from .file import load_config, load_constants

config = load_config()
constants = load_constants()
VERSION = "2.1.1"

TTT_ROUND_REGEX = re.compile(constants["ttt"]["regex"]["round"])
TTT_TIME_REGEX = re.compile(constants["ttt"]["regex"]["time"])
TTT_DAMAGE_REGEX = re.compile(constants["ttt"]["regex"]["damage"])
TTT_KILL_REGEX = re.compile(constants["ttt"]["regex"]["kill"])

STATUS_REGEX = re.compile(constants["age"]["regex"])
CONNECTED_REGEX = re.compile(constants["connected_regex"])

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

colours = {
    "black": Fore.BLACK,
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "white": Fore.WHITE,
}
RESET_COLOUR = Fore.RESET


def get_colour(setting_name: str):
    key, colour = None, None
    if not config["colours"]["enable"]:
        return ""
    try:
        key = config["colours"][setting_name].lower()
        return colours[key]
    except KeyError as e:
        raise ValueError(
            "Invalid colour name '{}' for '{}'".format(key, setting_name)
        ) from e


def colourify(setting_name: str, value: any):
    return "{}{}{}".format(get_colour(setting_name), value, RESET_COLOUR)
