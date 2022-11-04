Frequently Asked Questions
===========================

I'm getting python or pip is not recognized as an internal or external command
-----------------------------------------------------------------------------------

Make sure that it was installed properly, that you checked *Add to PATH* during the initial installation process, and
that you didn't use the Windows/Microsoft Store version. If you did any any of those, uninstall and reinstall Python, if
it still doesn't work, you can try to email me or contact me on Discord to resolve it. I'd recommend Googling first
though as it's highly likely someone's already had the exact same issue as you did.

I messed up something in the settings, what should I do?
--------------------------------------------------------------

Delete the ``settings.yaml`` file, and it'll be regenerated with default values. You'll have to change the settings
again to the values you want and fill in the API key again however.

I messed with the constants file, and now the program isn't parsing lines correctly
----------------------------------------------------------------------------------------

Delete the ``constants.yaml`` file, and it'll be regenerated with the proper working default values.

Can I add more GameME server IPs to playtime detection?
--------------------------------------------------------
Yes, provided that they're under the same GameME page as the existing entries, you can. To do so, go to
``constants.yaml``, go to ``age`` -> ``gameme`` -> ``game_code``. You can then add the IP you want in the following
format:

``{ip here}: {game code here}``

Replace ``{ip here}`` with the IP address of the server you wish to add, and replace ``{game code here}`` with the
GameME game code of the specific server you want to add (to get this, go to the GameME page of the server you want to
add and look at the URL, it'll be visible after the domain. For example ``csgo3`` is the gamecode in the URL
``prestigegaming.gameme.com/csgo3``)

Early Vents keeps showing despite no CT breaking vents
---------------------------------------------------------

There is a bug that occurs on some JB maps in which when a CT opens cells, it gets counted as breaking a vent or wall.
There is a feature that attempts to mitigate this by checking if the last action was the CT pressing a button, but this isn't foolproof.


Why shouldn't I double click to run STonitor?
-------------------------------------------------

This works just fine in most use cases, but if the program crashes or you close it, all output will be instantly gone.
You won't be able to see it again, normally closing is fine as STonitor will ask you confirm closing but not for errors.
Whether or not you decide to run STonitor by double-clicking is your choice, but using command prompt really isn't that
inconvenient (if you use a Batch file, it's actually more convenient!). When using command prompt, the past output still
shows until you close the command prompt window.

How was the name STonitor chosen?
------------------------------------
Since the idea for STonitor came from MSWS' Sonitor, I based the name of the program off of that. Sonitor didn't support
TTT while I was planning for STonitor to support it, so I added a T for TTT into the name. It was put after the S so
that it was in the order ST, representing Special Treatment for JB. In the end, it's just me being uncreative and not
wanting to come up with a new name.

Where is the data folder?
----------------------------

On versions 2.2.0 and above, all data is in the standard config directory for your operating system, under a subfolder
named "STonitor". On Windows, this is ``C:\Users\Username\AppData\Roaming\STonitor``.
On Linux and Mac, this is ``~/.config/STonitor``.

.. deprecated:: 2.2.0
    Prior to version 2.2.0, the data folder was in the same directory as the executable. This is no longer the case (see above).

How do I update STonitor?
---------------------------

Extract the new/updated ZIP file into where you originally installed STonitor and override if prompted. There may also
be additional instructions in the release notes for that version, make sure to look through them (and also the release
notes of any versions you skipped). Most commonly, these will be telling you to delete ``constants.yaml``,
``session.json``, or ``age_cache.json``.

How do I downgrade STonitor?
------------------------------

It's not recommended to downgrade Sonitor, as there may be unfixed bugs, and other issues in previous versions. If you
still want to, delete all files not in the ``data`` folder and then extract the ZIP file of the older version there.
Try to run it, but if you encounter an error than that likely means that the data files aren't compatible either. You'll
need to delete the data folder as well and re-configure them as if you were installing STonitor anew.

An invalid line keeps crashing STonitor, how can I resolve it?
-----------------------------------------------------------------

You can open the output.log file manually and wipe everything in it, then restart STonitor. If it was an issue with some
corrupted log/output, this will fix it. It's also recommended to :ref:`report it as a bug<How can I report a bug?>` so
that I can fix it within the program and prevent it from happening again.

.. versionadded:: 1.0.1
    STonitor will now automatically wipe output.log on error if the config option ``clear_on_error`` is true.

How can I report a bug?
--------------------------

Report a bug on GitHub using the Bug Report issue template, here's
`a link to make things easier <https://github.com/BLANK-TH/STonitor/issues/new?assignees=BLANK-TH&labels=bug&template=bug-report.md&title=>`_.
You'll need to have a GitHub account in order to do this. If you're unsure about any of the fields/sections in the
template, feel free to leave it blank. A bug report that isn't complete is better than no bug report.

How can I suggest a feature?
-------------------------------

Suggest a feature on GitHub using the Feature Request issue template, here's
`a link to make things easier <https://github.com/BLANK-TH/STonitor/issues/new?assignees=BLANK-TH&labels=enhancement&template=feature-request.md&title=>`_.
You'll need to have a GitHub account in order to do this.

Where can I contact the developer?
------------------------------------

If you came from eGO forums, you can feel free to reply to the thread there. You can also email me at
`contact[at]blankdvth.com <mailto:contact@blankdvth.com>`_.
