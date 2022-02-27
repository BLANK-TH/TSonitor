Known Bugs
============
Bugs that are currently known about the program, recommended to check this page in ``latest`` view for the most up to
date information.

Logs Parsing
-------------
JB
^^^
* LR/LG detection can be incorrect for any one of the following reasons, there's no practical way to eliminate all of these issues:
    * If someone does absolutely nothing that gets logged in the entire round, it will break LR/LG detection
    * If someone joins in the middle of the round and runs !ghost
* If someone gets respawned in the middle of the round, STonitor will ignore all logs about that person from their
death point forward. This is an unintentional side-effect of an intentional feature.

TTT
^^^^

Status Parsing
----------------
* When parsing a very long status, ``#end`` doesn't output properly, this is an issue with CS:GO.
