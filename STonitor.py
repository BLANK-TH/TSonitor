# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import os
import sys
from datetime import datetime
from time import sleep, time
from tkinter import Tk
from tkinter.messagebox import askyesno
from traceback import format_exception
from webbrowser import open as wbopen

import colorama
import requests
from packaging import version
from requests.exceptions import HTTPError
from steam.webapi import WebAPI

from helpers.file import (
    assert_data,
    check_output,
    load_age_cache,
    load_buttons,
    save_age_cache,
)


def except_hook(exc_class, message, traceback):
    """Global exception handler"""
    if exc_class is KeyboardInterrupt:
        graceful_exit()
    else:
        formatted = "".join(format_exception(exc_class, message, traceback))
        print(
            "==================== [ ERROR OCCURRED ] ====================\nError Name: {}\nError Message: {}\n{}---\n"
            "If this keeps happening, report a bug here: https://s.blankdvth.com/UU6CXoJb\n"
            "===========================================".format(
                exc_class.__name__, message, formatted
            )
        )
        with open("data/errors.txt", "a") as f:
            f.write(
                "=====\n{}\n---\n{}\n=====".format(
                    datetime.utcnow().strftime("%b %d, %Y %H:%M:%S UTC"), formatted
                )
            )


def graceful_exit():
    """Perform proper exit operations"""
    try:
        if config["confirm_exit"]:
            input("Press enter to exit the program...")
    except (Exception,):
        pass
    sys.exit()


def handle_ttt_log(logs):
    """Create and parse TTT logs from raw TTT lines"""
    try:
        log = parse_ttt_logs(
            logs,
            constants["ttt"]["log_separator"] + "\n" + constants["ttt"]["log_header"],
            ((constants["ttt"]["log_separator"] + "\n") * 2).rstrip(),
        )
    except ValueError as e:
        print("Error handling TTT logs, bad or corrupted log: " + str(e))
        return
    print(
        config["header"]
        + "\nTTT Logs (#{})\n".format(log.id)
        + log.summary_output(**config["logs"]["ttt"]["summary_output"]),
        end="\n\n",
    )
    if config["logs"]["ttt"]["subfeatures"]["rdm"]:
        rdms = log.find_rdm(config["logs"]["ttt"]["limits"]["rdm_detect_reason"])
        if len(rdms) > 0:
            print("Potential RDM(s):")
            for action in rdms:
                print(
                    "{} may have RDMed {}".format(
                        repr(action.attacker), repr(action.victim)
                    )
                )
            print("")
    if config["logs"]["ttt"]["subfeatures"]["mass_rdm"]:
        mass_rdms = log.find_mass_rdm(
            config["logs"]["ttt"]["limits"]["mass_rdm"],
            config["logs"]["ttt"]["limits"]["mass_rdm_detect_reason"],
        )
        if len(mass_rdms) > 0:
            print("Potential Mass RDM(s):")
            for player, count in mass_rdms.items():
                print(
                    "{} may have RDMed {} people".format(
                        repr(player), colourify("damage", f"{count:,}")
                    )
                )
            print("")
    if config["logs"]["ttt"]["subfeatures"]["inno_utility"]:
        inno_utility = log.find_innocent_utility(
            constants["ttt"]["utility_weapon_names"],
            config["logs"]["ttt"]["limits"]["utility_bad_only"],
        )
        if len(inno_utility) > 0:
            print("Innocent Utility Damage:")
            for player, counts in inno_utility.items():
                print(
                    "{} damaged {} Innocent(s), {} Detective(s), and {} Traitor(s) for a total of {} {}damage "
                    "using utility".format(
                        repr(player),
                        colourify("damage", "{:,}".format(counts[0])),
                        colourify("damage", "{:,}".format(counts[1])),
                        colourify("damage", "{:,}".format(counts[2])),
                        colourify("damage", "{:,}".format(counts[3])),
                        "bad "
                        if config["logs"]["ttt"]["limits"]["utility_bad_only"]
                        else "",
                    )
                )
            print("")
    if config["logs"]["save_logs"]:
        log.save_log()


def handle_jb_log(logs, round_number, buttons):
    """Create and parse JB logs from raw JB lines"""
    log = parse_jb_logs(
        logs,
        round_number,
        buttons,
        "\n".join(constants["jb"]["log_header"]),
        "\n".join(constants["jb"]["log_separator"]),
    )
    print(
        config["header"]
        + "\nJB Logs ({})\n".format(round_number)
        + log.summary_output(**config["logs"]["jb"]["summary_output"]),
        end="\n\n",
    )
    if config["logs"]["jb"]["subfeatures"]["wardenless_kill"]:
        kills = log.find_wardenless_fk(config["logs"]["jb"]["limits"]["freeday_delay"])
        if len(kills) > 0:
            print("Wardenless Freekills:")
            for kill in kills:
                print(
                    "{} killed {} without a warden".format(
                        repr(kill.attacker), repr(kill.victim)
                    )
                )
            print("")
    if config["logs"]["jb"]["subfeatures"]["new_warden_kill"]:
        kills = log.find_new_warden_fk(config["logs"]["jb"]["limits"]["warden"])
        if len(kills) > 0:
            print("New Warden Kills:")
            for kill in kills:
                print(
                    "{} killed {} without {:,} seconds given".format(
                        repr(kill.attacker),
                        repr(kill.victim),
                        config["logs"]["jb"]["limits"]["warden"],
                    )
                )
            print("")
    if config["logs"]["jb"]["subfeatures"]["early_vent"]:
        vents = log.find_early_vent()
        if len(vents) > 0:
            print("Early CT Vents:")
            for player in vents:
                print(
                    "{} broke a wall or vent before any prisoner did".format(
                        repr(player)
                    )
                )
            print("")
    if config["logs"]["jb"]["subfeatures"]["gunplant"]:
        gunplants = log.find_gunplant(config["logs"]["jb"]["limits"]["gunplant"])
        if len(gunplants) > 0:
            print("Potential Gunplants:")
            for gunplant in gunplants:
                print(
                    "{} dropped a(n) {} and {} used one shortly after".format(
                        repr(gunplant["ct"]),
                        colourify("weapon_name", gunplant["weapon"]),
                        repr(gunplant["t"]),
                    )
                )
            print("")
    if config["logs"]["jb"]["subfeatures"]["button_grief"]:
        griefs = log.find_button(
            config["logs"]["jb"]["limits"]["button"],
            config["logs"]["jb"]["limits"]["world_damage_threshold"],
            config["logs"]["jb"]["limits"]["ignore_warden_button"],
        )
        if len(griefs) > 0:
            print("Potential Button Griefs:")
            longest_name = str(
                len(repr(max(griefs.keys(), key=lambda x: len(repr(x.player))).player))
                + 2
            )
            longest_button = str(
                len(
                    repr(
                        max(
                            griefs.keys(), key=lambda x: len(x.button_str())
                        ).button_str()
                    )
                )
            )
            for button, grief in griefs.items():
                print(
                    (
                        "{:"
                        + longest_name
                        + "s} pressed {:"
                        + longest_button
                        + "s} and {} T(s) and {} CT(s) "
                        "might've been harmed"
                    ).format(
                        repr(button.player),
                        colourify("button_name", button.button_str()),
                        colourify("damage", f"{grief['t']:,}"),
                        colourify("damage", f"{grief['ct']:,}"),
                    )
                )
            print("")
    if config["logs"]["jb"]["subfeatures"]["nades"]:
        nades = log.find_utility(
            config["logs"]["jb"]["limits"]["nade"],
            config["logs"]["jb"]["limits"]["world_damage_threshold"],
        )
        if len(nades) > 0:
            print("Potential Nade Disruptions:")
            longest_name = str(
                len(repr(max(nades.keys(), key=lambda x: len(repr(x.player))).player))
                + 2
            )
            for util, grief in nades.items():
                print(
                    (
                        "{:"
                        + longest_name
                        + "s} threw a {} which could've disrupted {} T(s) and {} CT(s)"
                    ).format(
                        repr(util.player),
                        colourify("weapon_name", util.type),
                        colourify("damage", f"{grief['t']:,}"),
                        colourify("damage", f"{grief['ct']:,}"),
                    )
                )
            print("")
    if config["logs"]["jb"]["subfeatures"]["mass_freedamage"]:
        mfds = log.find_utility_mfd(
            config["logs"]["jb"]["limits"]["mass_freedamage"],
            config["logs"]["jb"]["limits"]["mass_freedamage_threshold"],
            constants["jb"]["utility_weapon_names"],
        )
        if len(mfds) > 0:
            print("Potential Nade Mass Freedamages:")
            for util, mfd in mfds.items():
                print(
                    "{} threw a {} which could've mass freedamaged {} T(s)".format(
                        repr(util.player),
                        colourify("weapon_name", util.type),
                        colourify("damage", f"{mfd:,}"),
                    )
                )
            print("")
    if config["logs"]["save_logs"]:
        log.save_log()


def handle_status(logs, server_ip):
    """Process and retrieve status from raw status lines"""
    print(config["header"] + "\nProcessing status, this may take a while...")
    results = []
    cache = load_age_cache() if config["age"]["cache"] else {}
    for line in logs:
        if len(line.strip()) == 0:
            continue
        try:
            results.append(
                parse_status(
                    steam_api,
                    line,
                    STATUS_REGEX,
                    cache,
                    config["age"]["private"]["enabled"],
                    config["age"]["private"]["tries"],
                    config["age"]["subfeatures"]["csgo_playtime"],
                    config["age"]["subfeatures"]["server_playtime"],
                    constants["age"]["gameme"]["game_code"],
                    server_ip,
                    constants["age"]["gameme"]["playerinfo_url"],
                )
            )
        except (Exception,) as e:
            results.append(
                (
                    float("inf"),
                    "-1",
                    colorama.Fore.RESET + "Error: {} ({})".format(type(e).__name__, str(e)),
                    colorama.Fore.RESET + "Error parsing line: " + repr(line),
                    False,
                    None,
                    None,
                    None,
                )
            )
    results.sort()
    pad_age = str(len(colourify("age", max(results, key=lambda x: len(colourify("age", x[3])))[3])) + 2)
    pad_name = str(len(colourify("name", max(results, key=lambda x: len(colourify("name", x[2])))[2])) + 2)
    pad_num = str(len(max(results, key=lambda x: len(x[1]))[1]))
    for result in results:
        print(
            (
                "# {:"
                + pad_num
                + "s} {:"
                + pad_name
                + "s} {:1s}{:"
                + pad_age
                + "s} {}{}{}"
            )
            .format(
                result[1],
                colourify("name", result[2]),
                "~" if result[4] else "",
                colourify("age", result[3]),
                "(LVL: {}) ".format(colourify("level", result[5]))
                if result[5] is not None
                else "",
                "(GPT: {}) ".format(colourify("game_playtime", result[6]))
                if result[6] is not None
                else "",
                "(SPT: {}) ".format(colourify("server_playtime", result[7]))
                if result[7] is not None
                else "",
            )
            .rstrip()
        )
    if config["age"]["cache"]:
        save_age_cache(cache)


def get_bool_status(*args):
    return [True if not isinstance(i, bool) else i for i in args]


if __name__ == "__main__":
    os.chdir(
        sys.path[0]
    )  # Set CWD to this file in case clueless users run wo/ a proper working directory
    sys.excepthook = except_hook  # Setup custom exception handler
    asrep = assert_data()
    if asrep is not True:
        if isinstance(asrep, str):
            print("File integrity check failed, user input needed: " + asrep)
        else:
            print(
                "Missing or invalid data files found, an automatic creation/fix was attempted"
            )
        sys.exit()

    from helpers.gvars import (
        config,
        constants,
        colourify,
        VERSION,
        STATUS_REGEX,
        CONNECTED_REGEX,
    )
    from helpers.logs import parse_ttt_logs, parse_jb_logs, parse_status

    buttons = load_buttons()
    try:
        steam_api = WebAPI(key=config["steamkey"]) if config["steamkey"] != "" else None
    except HTTPError:
        print(
            "Error connecting to Steam API, check steam key or remove it for now (disables features requiring key)"
        )
        sys.exit()

    pe = check_output(config["output_file"])
    if isinstance(pe, Exception):
        print(
            "Received {} opening output file, check that the path is valid and you have proper permissions.".format(
                type(pe).__name__
            )
        )
        sys.exit()

    if config["update_check"]:
        # Check GitHub API endpoint
        resp = requests.get(
            "https://api.github.com/repos/"
            + constants["github_release_latest"].lstrip("https://github.com/")
        )
        # Check whether response is a success
        if resp.status_code == 200:
            resp_js = resp.json()
            # Check whether the version number of remote is greater than version number of local (to avoid dev conflict)
            if version.parse(resp_js["tag_name"]) > version.parse(VERSION):
                # Ask user whether they want to open the releases page
                Tk().withdraw()
                yn_resp = askyesno(
                    "New Version",
                    "A new version ({}) is available.\n\nPress yes to open page and no to ignore.\n"
                    "Update checking can be disabled in config.".format(
                        resp_js["tag_name"]
                    ),
                )
                if yn_resp:
                    wbopen(constants["github_release_latest"])

    # Set initial variable values
    parsing_ttt = False
    parsing_jb = False
    parsing_status = False
    server_ip = None
    parsed_ttt = []
    parsed_jb = []
    parsed_statuses = []
    logs = []
    last_time = time()
    i = 0

    # Initiate colorama and tell user program is ready
    colorama.init(autoreset=True)
    print("STonitor is ready, waiting for output...\n---")
    while True:
        try:
            # Open output file and read all contents line by line
            with open(
                config["output_file"], "r", encoding="utf-8", errors="replace"
            ) as f:
                for line in f.readlines():
                    line = line.strip()

                    # Multi parse edge check
                    if (
                        sum(get_bool_status(parsing_ttt, parsing_jb, parsing_status))
                        > 1
                    ):
                        print(
                            "==================== [ ERROR OCCURRED ] ====================\nMore than 1 active "
                            "parsing operation detected. All current parsing has been cancelled, logs may be ignored "
                            "and flushed.\n==========================================="
                        )
                        parsing_ttt, parsing_jb, parsing_status = False, False, False
                        logs = []
                        # Attempt to clear output.log if error occurs
                        if config["clear_on_error"]:
                            with open(config["output_file"], "w") as f2:
                                f2.write("")
                            break

                    # TTT Log Parsing
                    if config["logs"]["ttt"]["enable"]:
                        # If 1 footer line has been detected and the current line is final footer part, handle the log
                        # Else, continue parsing
                        if parsing_ttt is None:
                            if line == constants["ttt"]["log_separator"]:
                                if logs not in parsed_ttt:
                                    handle_ttt_log(logs)
                                    parsed_ttt.append(logs)
                                parsing_ttt = False
                                logs = []
                            else:
                                parsing_ttt = True
                        # If parsing TTT and encounter initial footer line, tell program to look for final footer line
                        elif parsing_ttt and line == constants["ttt"]["log_separator"]:
                            parsing_ttt = None
                        # Add line to logs list if parsing TTT
                        elif parsing_ttt:
                            logs.append(line)
                        # If line indicates the start of TTT logs, start parsing
                        elif line == constants["ttt"]["log_header"]:
                            parsing_ttt = True
                            continue

                    # JB Log Parsing
                    if config["logs"]["jb"]["enable"]:
                        # If parsing JB and encountered first footer line, tell program to look for next footer lines
                        if (
                            parsing_jb is True
                            and line == constants["jb"]["log_separator"][0]
                        ):
                            parsing_jb = -1
                            continue
                        # If looking for header lines, check that current line is the expected header line, if it
                        # matches, look for next header line. If it's the final header line, begin parsing
                        elif not isinstance(parsing_jb, bool) and 3 > parsing_jb > 0:
                            if line == constants["jb"]["log_header"][parsing_jb]:
                                if parsing_jb == 2:
                                    parsing_jb = True
                                else:
                                    parsing_jb += 1
                                continue
                            else:
                                parsing_jb = False
                        # If looking for footer lines, check that current line is the expected footer line, if it
                        # matches, look for next footer line. If it's the final footer line, begin handling
                        elif not isinstance(parsing_jb, bool) and 0 > parsing_jb > -3:
                            if (
                                line
                                == constants["jb"]["log_separator"][abs(parsing_jb)]
                            ):
                                if parsing_jb == -2:
                                    if logs not in parsed_jb:
                                        handle_jb_log(
                                            logs,
                                            datetime.now().strftime(
                                                "%b-%d-%Y_%H-%M-%S_%f"
                                            ),
                                            buttons,
                                        )
                                        parsed_jb.append(logs)
                                    parsing_jb = False
                                    logs = []
                                else:
                                    parsing_jb -= 1
                            else:
                                parsing_jb = True
                                logs.append(line)
                        # If not parsing and encountered first header line, tell program to look for next header lines
                        elif (
                            parsing_jb is False
                            and line == constants["jb"]["log_header"][0]
                        ):
                            parsing_jb = 1
                            continue
                        # Add line to logs list if parsing JB
                        elif parsing_jb is True:
                            logs.append(line)

                    # Status Log Parsing
                    if config["age"]["enable"]:
                        # If line is footer, stop parsing and start handling
                        if parsing_status and line == constants["age"]["footer"]:
                            if logs not in parsed_statuses:
                                handle_status(logs, server_ip)
                                parsed_statuses.append(logs)
                            parsing_status = False
                            logs = []
                        # Add line to logs list if parsing status
                        elif parsing_status:
                            logs.append(line)
                        # If line is header, begin parsing
                        elif line == constants["age"]["header"]:
                            parsing_status = True
                            continue
                        else:
                            # Check for server IP, always outputted before status. Cache most recent for use in parsing
                            r = CONNECTED_REGEX.findall(line)
                            if len(r) > 0:
                                server_ip = r[0]
            # Clear output.log if there's no unfinished parsing
            if config["clear_output_log"] and not parsing_ttt and not parsing_jb:
                if parsing_status:
                    print(
                        "\n---\nStatus still parsing after log ended, incomplete or missing footer?"
                    )
                with open(config["output_file"], "w") as f:
                    f.write("")
                parsed_ttt = []
                parsed_jb = []
                parsed_statuses = []

            # Reset variables for next iteration
            parsing_ttt = False
            parsing_jb = False
            parsing_status = False
            logs = []

            sleep(config["check_delay"])
        except (Exception,) as e:
            sys.excepthook(type(e), e, e.__traceback__)  # Handle errors
            if (
                i >= constants["error_threshold"]
            ):  # Exit program if it's crashed more than X times
                break
            else:
                # Attempt to clear output.log if error occurs
                if config["clear_on_error"]:
                    try:
                        with open(config["output_file"], "w") as f:
                            f.write("")
                    except (Exception,) as e:
                        print(
                            "Failed to automatically clear output.log with {} {}".format(
                                type(e).__name__, str(e)
                            )
                        )
                # Increment crash counter and attempt to restart program by ignoring error
                i += 1
                print(
                    "Attempting to automatically restart the program, if it closes, this has failed. It's "
                    "recommended to close and re-open the program for a manual restart/reset."
                )

    print("Program exiting, errored out {:,} times".format(i))
    graceful_exit()
