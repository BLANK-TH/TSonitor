Settings
=========
Here's a list of all of the currently available settings parameters, and what they do

- **output_file**: *Full path to where the CS:GO output.log file is located, the prefilled value is the default for most people*. Default Value: ``C:/Program Files (x86)/Steam/steamapps/common/Counter-Strike Global Offensive/csgo/output.log``
- **steamkey**: *Your steam API key, needed to use the account age and CS:GO playtime features*. Example Value: ``12345A789101234FJ32U``
- **check_delay**: *The delay in between the program checking the output.log file for new contents, in seconds. The lower it is the faster you get results but the more resources the program uses.*. Default Value: ``5``
- **clear_output_log**: *Boolean (true/false) of whether output.log should be cleared once STonitor is done with it, this prevents repeat output (a runtime caching solution is implemented for JB & Status and a round number session solution for TTT in the case that you turn this off)*. Default Value: ``true``
- **clear_on_start**: *Boolean (true/false) of whether output.log should be cleared when STonitor starts.* Default Value: ``false``
- **clear_on_error**: *Boolean (true/false) of whether output.log is automatically cleared on error to attempt to fix corrupted log issues. Upside is less crashes, downside is potential lost log.*. Default Value: ``true``
- **confirm_exit**: *Boolean (true/false) of whether the program will ask you to confirm exiting by pressing enter. This may not work in all cases (certain errors at certain locations will bypass this)*. Default Value: ``true``
- **update_check**: *Boolean (true/false) of whether the program will check for newer versions on run*. Default Value: ``true``
- **constants_check**: *Boolean (true/false) of whether the program will check for non-expected constants on run*. Default Value: ``true``
- **show_disclaimer**: *Boolean (true/false) of whether the program will show a disclaimer when it starts*. Default Value: ``true``
- **header**: *The header that gets outputted before each program output session/log analysis. In order to create new lines, just press enter to make a new line as you would in any other file. This value must be in single quotes (')*. Example Value: ``====================``
- *logs*:
    - **save_logs**: *Boolean (true/false) of whether logs should be saved to a .txt file for archival purposes*. Default Value: ``true``
    - *jb*:
        - **enable**: *Boolean (true/false) of whether JB log analysis should be enabled*. Default Value: ``true``
        - *subfeatures*: :sup:`Boolean (true/false) toggles for whether each subfeature in JB log analysis is enabled`\
            - **early_vent**: *Notifies when a CT breaks vents before any prisoner does*. Default Value: ``true``
            - **wardenless_kill**: *Notifies when a CT kills a non-rebelling T without a warden*. Default Value: ``true``
            - **new_warden_kill**: *Notifies when a CT kills a non-rebelling T within X seconds of someone becoming warden, X is set in the limits section*. Default Value: ``true``
            - **st_kill**: *Notifies when a CT kills an ST*. Default Value: ``true``
            - **button_grief**: *Notifies when someone presses a button and players take more than X damage from the world within Y seconds, X and Y are set in limits*. Default Value: ``true``
            - **nades**: *Notifies when someone throws a nade/utility (flash, HE, molotov, etc) and players take more than X damage from the world within Y seconds, X and Y are set in limits.*. Default Value: ``true``
            - **mass_freedamage**: *Notifies when a CT throws a nade and more than X Ts take damage within Y seconds, X and Y are set in limits*. Default Value: ``true``
            - **gunplant**: *Notifies when a T picks up a CT's weapon before that CT dies*. Default Value: ``true``
        - *limits*: :sup:`Various configuration values for the sub-features above`\
            - **button**: *Number of seconds after someone presses a button that the program will be looking for damage from the world*. Default Value: ``10``
            - **nade**: *Number of seconds after someone throws utility that the program will be looking for damage from the world*. Default Value: ``10``
            - **warden**: *Number of seconds after someone becomes warden that the program will be looking for potential freekills*. Default Value: ``5``
            - **freeday_delay**: *Number of seconds after warden passes or gets fired that the program will begin looking for potential freekills*. Default Value: ``10``
            - **mass_freedamage**: *Number of seconds after a CT throws a nade that the program will be looking for Ts taking damage from that person using that nade*. Default Value: ``5``
            - **mass_freedamage_threshold**: *Number of unique players that take damage from a CT's nade before it's considered potential mass freedamage*. Default Value: ``4``
            - **world_damage_threshold**: *Minimum amount of damage for someone to take from the world for it to be considered in button grief detection and nade disruption detection*. Default Value: ``15``
            - **ignore_warden_button**: *Boolean (true/false) of whether warden is counted in button grief detection*. Default Value: ``true``
        - *summary_output*: :sup:`Boolean (true/false) to enable various types of actions to be shown in the JB summary output`\
            - **kills**: *Whether kills are shown in the JB summary output*. Default Value: ``true``
            - **warden**: *Whether someone becoming warden is shown in the JB summary output*. Default Value: ``true``
            - **warden_death**: *Whether warden dying is shown in the JB summary output*. Default Value: ``true``
            - **pass_fire**: *Whether warden passing or being fired is shown in the JB summary output*. Default Value: ``true``
            - **damage**: *Whether someone being damaged is shown in the JB summary output*. Default Value: ``false``
            - **vents**: *Whether someone breaking vents is shown in the JB summary output*. Default Value: ``false``
            - **button**: *Whether someone pressing a button is shown in the JB summary output*. Default Value: ``false``
            - **drop_weapon**: *Whether someone dropping a weapon is shown in the JB summary output, note that CTs dying counts as them dropping their weapons (don't worry, gunplant detection handles this)*. Default Value: ``false``
            - **pickup_weapon**: *Whether someone picking up a weapon is shown in the JB summary output*. Default Value: ``false``
            - **world**: *Whether to show an action if the attacker is the world (game deaths/fall damage deaths)*. Default Value: ``true``
    - *ttt*:
        - **enable**: *Boolean (true/false) of whether TTT log analysis should be enabled*. Default Value: ``true``
        - *subfeatures*: :sup:`Boolean (true/false) toggles for whether each subfeature in TTT log analysis is enabled`\
            - **rdm**: *Notifies when a player may have RDMed someone. By default, reason will be detected (configurable in limits)*. Default Value: ``true``
            - **mass_rdm**: *Notifies when a player may have mass RDMed. By default, reason will not be detected (configurable in limits)*. Default Value: ``true``
            - **inno_utility**: *Notifies when an innocent or detective throws utility and someone gets damaged by it*. Default Value: ``true``
            - **wallhack_purchase**: *Notifices when a Traitor purchases wallhack*. Default Value: ``true``
        - *limits*: :sup:`Various configuration values for the sub-features above`\
            - **rdm_detect_reason**: *Boolean (true/false) of whether reason is detected for normal RDMs. All reason detection is is going back in logs to check if the victim of an RDM attacked/damaged the attacker/potential RDMer first. If they did, it's not considered RDM*. Default Value: ``true``
            - **mass_rdm**: *Number of RDMs for a player to be considered Mass RDMing*. Default Value: ``2``
            - **mass_rdm_detect_reason**: *Boolean (true/false) of whether reason is detected for mass RDMs. See description of ``rdm_detect_reason`` for how reason detection works*. Default Value: ``false``
            - **utility_bad_only**: *Boolean (true/false) of whether only bad damage is counted for inno utility detection*. Default Value: ``false``
        - *summary_output*: :sup:`Boolean (true/false) to enable various types of actions to be shown in the TTT summary output`\
            - **kills**: *Whether kills are shown in the TTT summary output*. Default Value: ``true``
            - **damage**: *Whether damage is shown in the TTT summary output*. Default Value: ``false``
            - **id**: *Whether body IDing is shown in the TTT summary output*. Default Value: ``false``
            - **dna_scan**: *Whether Detective DNA scans are shown in the TTT summary output*. Default Value: ``false``
            - **tase**: *Whether tasing is shown in the TTT summary output*. Default Value: ``true``
            - **shop**: *Whether shop purchases are shown in the TTT summary output*. Default Value: ``false``
- *age*: :sup:`Steam account age, CS:GO playtime, and server playtime`\
    - **enable**: *Boolean (true/false) of whether status/age detection should be enabled*. Default Value: ``true``
    - **cache**: *Boolean (true/false) of whether to cache account ages (this significantly minimizes the number of API calls, speeding the program up significantly)*. Default Value: ``true``
    - *subfeatures*: :sup:`Boolean (true/false) toggles for whether each subfeature in TTT log analysis is enabled`\
        - **csgo_playtime**: *Whether CS:GO playtime for accounts is retrieved (when available)*. Default Value: ``true``
        - **server_playtime**: *Whether server playtime for accounts is retrieved*. Default Value: ``true``
    - *private*: :sup:`Configuration options specifically for private accounts`\
        - **enabled**: *Boolean (true/false) of whether private account age guessing is enabled. This is done by checking the account ages of accounts made immediately after the private account to estimate the age of the private account*. Default Value: ``true``
        - **tries**: *Number of tries for private account age detection (number of accounts after private account) to try before giving up*. Default Value: ``10``
- *colours*: :sup:`Settings regarding coloured output of STonitor. Valid colours are black, red, green, yellow, blue, magenta, cyan, and white`\
    - **enable**: *Boolean (true/false) of whether output should be coloured*. Default Value: ``true``
    - **time**: *Colour for outputs related to time*. Default Value: ``cyan``
    - **name**: *Colour for player names*. Default Value: ``magenta``
    - **button_name**: *Colour for names of buttons*. Default Value: ``yellow``
    - **weapon_name**: *Colour for names and types of weapons*. Default Value: ``yellow``
    - **damage**: *Colour for damage numbers (points of damage, number of players damaged/killed, etc)*. Default Value: ``red``
    - **role**: *Colour for player role names. This setting can be set to "automatic", in which the colour will be based off of their role. This can cause overlap of colours*. Default Value: ``automatic``
    - **age**: *Colour for player steam account age in Steam Age output*. Default Value: ``cyan``
    - **level**: *Colour for player level in Steam Age output*. Default Value: ``red``
    - **game_playtime**: *Colour for playtime of game in Steam Age output*. Default Value: ``yellow``
    - **server_playtime**: *Colour for playtime on the server in Steam Age output*. Default Value: ``green``

.. versionchanged:: 2.1.1
    Removed ``jb``/``limits``/``gunplant`` as new gunplant detection system no longer uses it

.. versionchanged:: 1.0.1
    Removed ``min_session_save_interval`` as session is no longer used
