# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import os
import sys

from helpers.file import assert_data, load_config

if __name__ == '__main__':
    os.chdir(sys.path[0])  # Set CWD to this file in case clueless users run wo/ a proper working directory
    if not assert_data():
        print("Missing or invalid data files found, an automatic creation/fix was attempted, please check data files "
              "for potential needed user input")
        sys.exit()
    config = load_config()
