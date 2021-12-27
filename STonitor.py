# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import os
import sys
from time import sleep, time

from helpers.file import assert_data, load_config, load_session, save_session

def handle_ttt_log(logs):
    log = parse_ttt_logs(logs)
    print(config["logs"]["header"] + '\nTTT Logs (#{})\n'.format(log.id) +
          log.summary_output(**config["logs"]["ttt"]["summary_output"]), end='\n\n')
    if config["logs"]["ttt"]["subfeatures"]["rdm"]:
        rdms = log.find_rdm(config["logs"]["ttt"]["limits"]["rdm_detect_reason"])
        if len(rdms) > 0:
            print("Potential RDM(s):")
            for action in rdms:
                print("{} may have RDMed {}".format(action.attacker, action.victim))
            print('\n')
    if config["logs"]["ttt"]["subfeatures"]["mass_rdm"]:
        mass_rdms = log.find_mass_rdm(config["logs"]["ttt"]["limits"]["mass_rdm"],
                                      config["logs"]["ttt"]["limits"]["mass_rdm_detect_reason"])
        if len(mass_rdms) > 0:
            print("Potential Mass RDM(s):")
            for player, count in mass_rdms.items():
                print("{} may have RDMed {:,} people".format(player.name, count))
            print('\n')
    if config["logs"]["save_logs"]:
        log.save_log()


if __name__ == '__main__':
    os.chdir(sys.path[0])  # Set CWD to this file in case clueless users run wo/ a proper working directory
    if not assert_data():
        print("Missing or invalid data files found, an automatic creation/fix was attempted, please check data files "
              "for potential needed user input")
        sys.exit()

    from helpers.gvars import constants, TTT_ROUND_REGEX
    from helpers.logs import parse_ttt_logs

    config = load_config()
    session = load_session()

    current_ttt_round = session.get('last_ttt_round', float('-inf'))
    current_jb_round = session.get('last_jb_round', float('-inf'))
    parsing_ttt = False
    parsing_jb = False
    last_time = time()
    logs = []
    while True:
        with open(config['output_file'], 'r', errors='replace') as f:
            for line in f.readlines():
                line = line.strip()

                # TTT Log Parsing
                if parsing_ttt and len(logs) == 0:
                    round_number = int(TTT_ROUND_REGEX.findall(line)[0])
                    if round_number <= current_ttt_round:
                        parsing_ttt = False
                        continue
                    logs.append(line)
                elif parsing_ttt is None:
                    if line == constants["ttt"]["log_separator"]:
                        parsing_ttt = False
                        handle_ttt_log(logs)
                        logs = []
                        current_ttt_round = round_number
                        session["last_ttt_round"] = round_number
                    else:
                        parsing_ttt = True
                elif parsing_ttt and line == constants["ttt"]["log_separator"]:
                    parsing_ttt = None
                elif parsing_ttt:
                    logs.append(line)
                elif line == constants["ttt"]["log_header"]:
                    parsing_ttt = True
                    continue

                # JB Log Parsing

                # Status Log Parsing

        parsing_ttt = False
        parsing_jb = False
        logs = []

        current_time = time()
        if current_time - last_time >= config["min_session_save_interval"]:
            save_session(session)
            last_time = current_time
        sleep(config["check_delay"])
