# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import os
import sys
from time import sleep, time

from steam.webapi import WebAPI
from requests.exceptions import HTTPError

from helpers.file import assert_data, load_config, load_session, save_session, load_age_cache, save_age_cache

def handle_ttt_log(logs):
    log = parse_ttt_logs(logs)
    print(config["header"] + '\nTTT Logs (#{})\n'.format(log.id) +
          log.summary_output(**config["logs"]["ttt"]["summary_output"]), end='\n\n')
    if config["logs"]["ttt"]["subfeatures"]["rdm"]:
        rdms = log.find_rdm(config["logs"]["ttt"]["limits"]["rdm_detect_reason"])
        if len(rdms) > 0:
            print("Potential RDM(s):")
            for action in rdms:
                print("{} may have RDMed {}".format(repr(action.attacker), repr(action.victim)))
            print('')
    if config["logs"]["ttt"]["subfeatures"]["mass_rdm"]:
        mass_rdms = log.find_mass_rdm(config["logs"]["ttt"]["limits"]["mass_rdm"],
                                      config["logs"]["ttt"]["limits"]["mass_rdm_detect_reason"])
        if len(mass_rdms) > 0:
            print("Potential Mass RDM(s):")
            for player, count in mass_rdms.items():
                print("{} may have RDMed {:,} people".format(repr(player), count))
            print('')
    if config["logs"]["ttt"]["subfeatures"]["inno_utility"]:
        inno_utility = log.find_innocent_utility(constants["ttt"]["utility_weapon_names"],
                                                 config["logs"]["ttt"]["limits"]["utility_bad_only"])
        if len(inno_utility) > 0:
            print("Innocent Utility Damage:")
            for player, counts in inno_utility.items():
                print("{} damaged {} Innocent(s), {} Detective(s), and {} Traitor(s) for a total of {:,} {}damage "
                      "using utility".format(repr(player), *counts, 'bad '
                if config["logs"]["ttt"]["limits"]["utility_bad_only"] else '',))
            print('')
    if config["logs"]["save_logs"]:
        log.save_log()


def handle_status(logs):
    print(config["header"])
    results = []
    cache = load_age_cache() if config["age"]["cache"] else {}
    for line in logs:
        try:
            results.append(parse_status(steam_api, line, STATUS_REGEX, cache, config["age"]["private"]["enabled"],
                                        config["age"]["private"]["tries"],
                                        config["age"]["subfeatures"]["csgo_playtime"]))
        except (Exception,):
            results.append((float('inf'), '-1', 'Error', 'Error parsing line: ' + line, False, 'None'))
    results.sort()
    pad_name = str(len(max(results, key=lambda x:len(x[2]))[2]) + 2)
    pad_num = str(len(max(results, key=lambda x:len(x[1]))))
    for result in results:
        print(('# {:' + pad_num + 's} {:' + pad_name + 's} {}{} {}').format(
            result[1], result[2], '~' if result[4] else '', result[3], '(GPT: {})'.format(
            result[5]) if result[5] != 'None' else ''))
    if config["age"]["cache"]:
        save_age_cache(cache)


if __name__ == '__main__':
    os.chdir(sys.path[0])  # Set CWD to this file in case clueless users run wo/ a proper working directory
    if not assert_data():
        print("Missing or invalid data files found, an automatic creation/fix was attempted, please check data files "
              "for potential needed user input")
        sys.exit()

    from helpers.gvars import constants, TTT_ROUND_REGEX, STATUS_REGEX
    from helpers.logs import parse_ttt_logs, parse_status

    config = load_config()
    session = load_session()
    try:
        steam_api = WebAPI(key=config["steamkey"]) if config["steamkey"] != '' else None
    except HTTPError:
        print("Error connecting to Steam API, check steam key or remove it for now (disables features requiring key)")
        sys.exit()

    current_ttt_round = session.get('last_ttt_round', float('-inf'))
    current_jb_round = session.get('last_jb_round', float('-inf'))
    parsing_ttt = False
    parsing_jb = False
    parsing_status = False
    last_time = time()
    parsed_statuses = []
    logs = []
    while True:
        with open(config['output_file'], 'r', errors='replace') as f:
            for line in f.readlines():
                line = line.strip()

                # TTT Log Parsing
                if config["logs"]["ttt"]["enable"]:
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
                if config["logs"]["jb"]["enable"]:
                    pass

                # Status Log Parsing
                if config["age"]["enable"]:
                    if parsing_status and line == constants["age"]["footer"]:
                        if logs not in parsed_statuses:
                            handle_status(logs)
                            parsed_statuses.append(logs)
                        parsing_status = False
                        logs = []
                    elif parsing_status:
                        logs.append(line)
                    elif line == constants["age"]["header"]:
                        parsing_status = True
                        continue

        parsing_ttt = False
        parsing_jb = False
        parsing_status = False
        logs = []

        current_time = time()
        if current_time - last_time >= config["min_session_save_interval"]:
            save_session(session)
            last_time = current_time
        sleep(config["check_delay"])
