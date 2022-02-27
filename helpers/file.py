# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from copy import deepcopy
from json import load, dump
from os import mkdir
from os.path import isfile, isdir
from re import compile as rcompile, error as rerror
from typing import Union

import yaml

default_settings = {
    "output_file": "C:/Program Files (x86)/Steam/steamapps/common/Counter-Strike Global Offensive/csgo/output.log",
    "steamkey": "",
    "check_delay": 5,
    "clear_output_log": True,
    "clear_on_error": True,
    "confirm_exit": True,
    "update_check": True,
    "header": "\n\n\n=================================",
    "logs": {
        "save_logs": True,
        "jb": {
            "enable": True,
            "subfeatures": {
                "early_vent": True,
                "wardenless_kill": True,
                "new_warden_kill": True,
                "button_grief": True,
                "nades": True,
                "mass_freedamage": True,
                "gunplant": True
            },
            "limits": {
                "gunplant": 20,
                "button": 10,
                "nade": 10,
                "warden": 5,
                "freeday_delay": 10,
                "mass_freedamage": 5,
                "mass_freedamage_threshold": 4,
                "world_damage_threshold": 15,
                "ignore_warden_button": True
            },
            "summary_output": {
                "kills": True,
                "warden": True,
                "warden_death": True,
                "pass_fire": True,
                "damage": False,
                "vents": False,
                "button": False,
                "drop_weapon": False,
                "world": True
            }
        },
        "ttt": {
            "enable": True,
            "subfeatures": {
                "rdm": True,
                "mass_rdm": True,
                "inno_utility": True
            },
            "limits": {
                "rdm_detect_reason": True,
                "mass_rdm": 2,
                "mass_rdm_detect_reason": False,
                "utility_bad_only": False
            },
            "summary_output": {
                "kills": True,
                "damage": False
            }
        }
    },
    "age": {
        "enable": True,
        "cache": True,
        "subfeatures": {
            "csgo_playtime": True,
            "server_playtime": True
        },
        "private": {
            "enabled": True,
            "tries": 10
        }
    }
}

constants = {
    "ttt": {
        "regex": {
            "round": r"^\[\d{1,2}:\d{1,2}] TTT Round #(\d*) has been started!$",
            "time": r"^\[(?P<time>\d{1,2}:\d{1,2})].*$",
            "damage": r"^\[(?P<time>\d{1,2}:\d{1,2})] -> \[(?P<attacker>.*) \((?P<attacker_role>Traitor|Detective|Innocent)\) damaged (?P<victim>.*) \((?P<victim_role>Traitor|Detective|Innocent)\) for (?P<damage>\d*) damage(?: \(HEADSHOT\))? with (?P<weapon>.*)](?: - BAD ACTION)?$",
            "kill": r"^\[(?P<time>\d{1,2}:\d{1,2})] -> \[(?P<attacker>.*) \((?P<attacker_role>Traitor|Detective|Innocent)\) killed (?P<victim>.*) \((?P<victim_role>Traitor|Detective|Innocent)\) with (?P<weapon>.*)](?: - BAD ACTION)?$"
        },
        "log_header": "---------------TTT LOGS---------------",
        "log_separator": "--------------------------------------",
        'utility_weapon_names': ['inferno', 'hegrenade_projectile']
    },
    "jb": {
        "regex": {
            "death": r"^\[(?P<time>\d{1,2}:\d{1,2})] (?P<attacker>.*?)(?: \((?P<attacker_role>Prisoner|Rebel|Guard|Warden|ST)\))? killed (?P<victim>.*) \((?P<victim_role>Prisoner|Rebel|Guard|Warden|ST)\)$",
            "damage": r"^\[(?P<time>\d{1,2}:\d{1,2})] (?P<attacker>.*?)(?: \((?P<attacker_role>Prisoner|Rebel|Guard|Warden|ST)\))? hurt (?P<victim>.*) \((?P<victim_role>Prisoner|Rebel|Guard|Warden|ST)\) with (?P<damage>\d*) damage \((?P<weapon>.*)\)$",
            "button": r"^\[(?P<time>\d{1,2}:\d{1,2})] (?P<player>.*) \((?P<player_role>Prisoner|Rebel|Guard|Warden|ST)\) pressed button '(?P<button_name>.*)'(?: \(#(?P<button_number>\d*)\))?$",
            "ventwall": r"^\[(?P<time>\d{1,2}:\d{1,2})] (?P<player>.*) \((?P<player_role>Prisoner|Rebel|Guard|Warden|ST)\) broke a vent or wall$",
            "utility": r"^\[(?P<time>\d{1,2}:\d{1,2})] (?P<player>.*) \((?P<player_role>Prisoner|Rebel|Guard|Warden|ST)\) threw a (?P<type>smoke|grenade|flash|decoy|molotov)$",
            "wardendeath": r"^\[(?P<time>\d{1,2}:\d{1,2})] (?P<player>.*) \(WARDEN\) has died and is no longer warden$",
            "newwarden": r"^\[(?P<time>\d{1,2}:\d{1,2})] (?P<player>.*) \(WARDEN\) is now warden$",
            "passfire": r"^\[(?P<time>\d{1,2}:\d{1,2})] (?P<player>.*) \(WARDEN\) (?:has passed warden|has disconnected, passing warden|has been fired by an admin)$",
            "weapondrop": r"^\[(?P<time>\d{1,2}:\d{1,2})] (?P<player>.*) \((?P<player_role>Prisoner|Rebel|Guard|Warden|ST)\) dropped the weapon (?P<weapon>.*)\.$",
            "time": r"^\[(?P<time>\d{1,2}:\d{1,2})].*$"
        },
        "log_header": [
            "--------------------------------------------------",
            "----------------[ JAILBREAK LOGS ]----------------",
            "--------------------------------------------------"
        ],
        "log_separator": [
            "--------------------------------------------------",
            "--------------[ JAILBREAK LOGS END ]--------------",
            "--------------------------------------------------"
        ],
        'utility_weapon_names': {'molotov': 'inferno', 'grenade': 'hegrenade'}
    },
    "age": {
        "regex": r"^# *(?P<user_id>\d*) \d* \"(?P<name>.*)\" (?P<steam_id>STEAM_\d:\d:\d*).+$",
        "header": "# userid name uniqueid connected ping loss state rate",
        "footer": "#end",
        "gameme": {
            "playerinfo_url": "https://edgegamersorg.gameme.com/r/playerinfo",
            "game_code": {"74.91.113.113:27015": 'csgo2', '74.91.113.83:27015': 'csgo3'}
        }
    },
    "connected_regex": r"^Connected to ([0-9\.:]*)$",
    "error_threshold": 10,
    "github_release_latest": "https://github.com/BLANK-TH/STonitor/releases/latest"
}

button_alias = {
    "normal": {
        "slthm_lever": {
            'ignore': True,
            'alias': None
        },
        'slthm_2_lever': {
            'ignore': True,
            'alias': None
        },
        'celldoors': {
            'ignore': True,
            'alias': 'Cell Button'
        },
        'cellbutton': {
            'ignore': True,
            'alias': 'Cell Button'
        },
        'deathcreate_stop': {
            'ignore': True,
            'alias': 'Deathcrate Stop'
        }
    },
    "regex": {
        r"piano_key_\ws?": {
            'ignore': True,
            'alias': "Piano Key"
        },
        r"gun_button_\d*": {
            'ignore': True,
            'alias': 'Gun Button'
        }
    }
}


def check_dict(d: dict, expected: dict, fixed_dict=None) -> Union[bool, dict]:
    """Goes through each dict and subdict to check if the keys in expected are in d, if not, they're filled in with the
    value in expected

    :param d: Dict to check
    :param expected: Dict with expected keys
    :param fixed_dict: Patched version of d
    :return: True if check succeeded, list of missing keys if check failed
    """
    if d is None:
        d = {}  # Set d to an empty dict if d is None, which happens when YAML file is empty
    if fixed_dict is None:
        fixed_dict = d.copy()  # Set fixed dict to be a copy of d if not provided in args
    else:
        fixed_dict = fixed_dict.copy()  # Set fixed dict to be a copy of one provided in args if given

    for k, v in expected.items():
        if k not in d.keys():
            fixed_dict[k] = expected[k]
        if isinstance(v, dict):
            sr = check_dict(d.get(k, {}), expected[k], fixed_dict[k])
            if isinstance(sr, dict):
                fixed_dict[k] = sr

    return True if fixed_dict == d else {k: fixed_dict[k] for k in expected}  # Hacky way to sort & remove unused keys


def assert_data() -> Union[bool, str]:
    """Checks if the data folder and required files exist, if not, create them

    :return: True if all data is correct, False if data was created/modified, str if additional info is provided
    """
    success = True

    if not isdir('data'):
        mkdir('data')
    if not isdir('data/logs'):
        mkdir('data/logs')
    if not isfile('data/settings.yaml'):
        with open('data/settings.yaml', 'w') as f:
            f.write(yaml.dump(default_settings, sort_keys=False))
        success = False
    else:
        r = check_dict(load_config(), default_settings)
        if isinstance(r, dict):
            with open('data/settings.yaml', 'w') as f:
                f.write(yaml.dump(r, sort_keys=False))
            success = False
    if not isfile('data/constants.yaml'):
        with open('data/constants.yaml', 'w') as f:
            f.write(yaml.dump(constants, sort_keys=False, width=float('inf')))
    else:
        r = check_dict(load_constants(), constants)
        if isinstance(r, dict):
            with open('data/constants.yaml', 'w') as f:
                f.write(yaml.dump(r, sort_keys=False, width=float('inf')))
    if not isfile('data/buttons.yaml'):
        with open('data/buttons.yaml', 'w') as f:
            f.write(yaml.dump(button_alias, sort_keys=False, width=float('inf')))
    else:
        btns = load_buttons()
        btns_working = deepcopy(btns)
        for k, v in btns['normal'].items():
            if 'ignore' not in v:
                btns_working['normal'][k]['ignore'] = False
            if 'alias' not in v:
                btns_working['normal'][k]['alias'] = None
        for k, v in btns['regex'].items():
            try:
                rcompile(k)
            except rerror:
                success = "Invalid regex in buttons.yaml: " + k
            if 'ignore' not in v:
                btns_working['regex'][k]['ignore'] = False
            if 'alias' not in v:
                btns_working['regex'][k]['alias'] = None

        if btns != btns_working:
            with open('data/buttons.yaml', 'w') as f:
                f.write(yaml.dump(btns_working, sort_keys=False, width=float('inf')))
    if not isfile('data/age_cache.json'):
        with open('data/age_cache.json', 'w') as f:
            dump({}, f, indent=2)
    if not isfile('data/errors.txt'):
        with open('data/errors.txt', 'w') as f:
            f.write('')

    return success


def check_output(path) -> Union[Exception, type(None)]:
    try:
        with open(path, 'r', encoding='utf-8'):
            pass
    except (Exception,) as e:
        return e


def load_config() -> dict:
    """Loads and parses the YAML config file

    :return: Config loaded from file
    """
    with open('data/settings.yaml', 'r') as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)


def load_constants() -> dict:
    """Loads and parses the YAML constants file

    :return: Constants loaded from file
    """
    with open('data/constants.yaml', 'r') as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)


def load_buttons() -> dict:
    """Loads and parses the YAML button configuration file

    :return: Button config loaded from file
    """
    with open('data/buttons.yaml', 'r') as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)


def load_age_cache() -> dict:
    """Loads and parses the age cache JSON file

    :return: Age cache loaded from file
    """
    with open('data/age_cache.json', 'r') as f:
        return load(f)


def save_age_cache(cache):
    """Updates the age cache JSON file"""
    with open('data/age_cache.json', 'w') as f:
        dump(cache, f, indent=2)
