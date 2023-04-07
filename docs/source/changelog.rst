Changelog
============
All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
------------
Added
^^^^^^^
* New log types to TTT Summary Output

    * Body IDing
    * Detective DNA Scans
    * Tasing
    * Shop Purchases

* Automatic checking for updated constants
* Add detection for wallhack purchases

Changed
^^^^^^^
* Added option to clear output.log on program start
* Cleaned up TTT implementation

Fixed
^^^^^^^
* Outdated default GameME link for eGO
* Ensured that users can see the FileNotFound error when searching for output.log
* Various minor errors in the documentation (spelling, old information, etc)

[2.2.0] - 2022-11-04
---------------------
Added
^^^^^^^
* Shows disclaimer on startup
* Created installer for Windows

Changed
^^^^^^^
* Added healthshot to gunplant ignore
* Updated GitHub update checking URL to new one
* Moved data folder to native data location (APPDATA, .config)
* Documentation updated to reference Windows installer
* The program now asks if you want to open the data folder if it generates it
* Clarify additional step in manual BAT setup instructions

Fixed
^^^^^^^
* Incorrect default colours listed in settings documentation
* Typo in default button config
* TTT summary output not showing damage dealt
* Edge case in which the program would crash if there was a specific issue retrieving account age
* Broken update checking as a result of repo URL change

[2.1.2] - 2022-05-15
------------------------
Changed
^^^^^^^^
* Default colours so that they're more readable with default Command Prompt

Removed
^^^^^^^^
* Unused colour ``playtime``

[2.1.1] - 2022-05-15
------------------------
Added
^^^^^
* jb_undertale pictionary draw button to default ignore
* Various entries regarding JB logging in the known bugs documentation page
* Coloured output to make wall of text easier to understand
* ST kill detection
* Summary output for weapon pickup

Changed
^^^^^^^^
* Better invalid status line logging
* Version number now shows in ready message
* Gunplant detection now simply checks if a T picks up a CT's weapon before that CT dies

Fixed
^^^^^
* Outdated default GameME link for eGO
* Space padding incorrect on button grief output
* Fix odd invalid status line error
* Typo in documentation index page

Removed
^^^^^^^
* Feature list is no longer shown in README

[2.0.1] - 2022-01-20
------------------------
Fixed
^^^^^
* Regex not matching status lines when space padded

[2.0.0] - 2022-01-20
------------------------
Added
^^^^^
* Clarification on common status issues in documentation
* Check if output.log exists at runtime
* Ability to hide world actions from summary output
* Steam level to status
* Basic support for new ``ST`` role in logs
* FAQ entry for new GameME detections
* Known bugs page on documentation
* Show error message on status error
* Button ignore & alias file

Changed
^^^^^^^^
* Output.log now opens in UTF-8 encoding
* Non-context roles now show as T/CT to avoid confusion
* Rewrote status parsing code to have less spaghetti
* Other retrievable options are still retrieved if account is private now

Fixed
^^^^^^
* KeyError on invalid weapon name (MFD Detection)
* Status getting stuck wo/ ``#end``
* Multi-parse edge cases causing odd bugs
* Early vent false positive on some maps

[1.1.2] - 2022-01-01
------------------------
Fixed
^^^^^^
* Damage regex not triggering if damage was headshot

[1.1.1] - 2021-12-31
------------------------
Added
^^^^^^
* Ability to retrieve server playtime using GameME

[1.0.1] - 2021-12-31
------------------------
Added
^^^^^^
* Ability to wipe output.log on error to try to automatically resolve errors arising from corrupted logs

Changed
^^^^^^^^^^
* Exempt potential FK/FD during LR and LG instead of just LG
* TTT now uses caching similar to status and JB
* Parsed arrays are now cleared as soon as output.log is cleared to minimize unneeded memory usage

Fixed
^^^^^^^
* LR detection reporting wrong death
* IndexError in case of corrupted TTT logs
* TTT full logs not being parsed if sm_logs was run during the round to retrieve partial log

Deprecated
^^^^^^^^^^^^
* ``session.json`` is no longer used, and can be removed

[1.0.0] - 2021-12-30
------------------------
Initial release, no changes
