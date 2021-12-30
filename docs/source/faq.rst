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

Early Vents keeps showing despite no CT breaking vents
---------------------------------------------------------

There is a bug that occurs on some JB maps in which when a CT opens cells, it gets counted as breaking a vent or wall.
Adding a feature to catch and ignore this is in the plans but currently doesn't exist.

How was the name STonitor chosen?
------------------------------------
Since the idea for STonitor came from MSWS' Sonitor, I based the name of the program off of that. Sonitor didn't support
TTT while I was planning for STonitor to support it, so I added a T for TTT into the name. It was put after the S so
that it was in the order ST, representing Special Treatment for JB. In the end, it's just me being uncreative and not
wanting to come up with a new name.

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
