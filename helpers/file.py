# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from typing import Union
from os import mkdir
from os.path import isfile, isdir

import yaml

default_settings = {
    "directory": "C:/Program Files (x86)/Steam/steamapps/common/Counter-Strike Global Offensive/csgo/output.log",
    "steamkey": "",
    "check_delay": 5,
    "logs": {
        "header": "\n\n\n=================================",
        "jb": {
            "enable": True,
            "subfeatures": {
                "early_vent": True,
                "wardenless_kill": True,
                "new_warden_kill": True,
                "button_grief": True,
                "nades": True,
                "gunplant": True
            },
            "timeouts": {
                "gunplant": 20,
                "button": 10,
                "nade": 10,
                "warden": 5,
                "freeday_delay": 10
            }
        },
        "ttt": {
            "enable": True
        }
    },
    "age": {
        "enable": True,
        "check_csgo_playtime": True,
        "cache": True,
        "guess_private": True,
        "timeout": 5
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

    return True if fixed_dict == d else {k:fixed_dict[k] for k in expected}  # Hacky way to sort dict

def assert_data() -> bool:
    """Checks if the data folder and required files exist, if not, create them

    :return: True if all data is correct, False if data was created/modified
    """
    if not isdir('data'):
        mkdir('data')
    if not isdir('data/logs'):
        mkdir('data/logs')
    if not isfile('data/settings.yaml'):
        with open('data/settings.yaml', 'w') as f:
            f.write(yaml.dump(default_settings, sort_keys=False))
        return False
    else:
        with open('data/settings.yaml', 'r') as f:
            r = check_dict(yaml.load(f.read(), Loader=yaml.FullLoader), default_settings)
        if isinstance(r, dict):
            with open('data/settings.yaml', 'w') as f:
                f.write(yaml.dump(r, sort_keys=False))

    return True
