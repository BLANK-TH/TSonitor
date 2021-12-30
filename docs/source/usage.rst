Usage
========

How to use JB Log Analysis
------------------------------

When a new JB log is detected in the console output, STonitor will automatically parse it and output data according
to each of it's sub-features. No manual user input is needed. It'll generally be in the format:

.. code-block::

    <header here>
    JB Logs (<date and time here (matches filename if saving is enabled)>)
    <summary output here>

    <sub-feature name>:
    <sub-feature output>

Sub-feature name and sub-feature output repeats for every enabled sub-feature that has at least 1 detection.

How to use TTT Log Analysis
-----------------------------

When a new TTT log is detected in the console output, STonitor will automatically parse it and output data according
to each of it's sub-features. No manual user input is needed. It'll generally be in the format:

.. code-block::

    <header here>
    TTT Logs (#<round number here>)
    <summary output here>

    <sub-feature name>:
    <sub-feature output>

Sub-feature name and sub-feature output repeats for every enabled sub-feature that has at least 1 detection.

How to use Log Saving
-------------------------

If enabled, logs are automatically saved to your computer. If you want to access these logs, open the data folder, then
the logs folder. Inside will be numerous text files. TTT text files are stored according to round number (the thing that
gets outputted at the start of every log), for example: ``TTT_123456.txt``. JB text files are stored according to
the date and time up to milliseconds of the log being parsed (milliseconds are there to prevent overwriting previous
logs in case your computer is too fast and your check interval is low), for example:
``JB_Dec-29-2021_15-19-56_773927.txt``.

How to use Steam Account Age Checking
----------------------------------------

Open up your CS:GO developer console, and type ``status`` while you're in a server. The program will detect it being
outputted and automatically parse and retrieve the desired data. This may take a while depending on how many people
are cached, how many are on the server, your internet speed, your computer specs, and what not. You will see a header
and the words ``Processing status, this may take a while...`` fairly quickly however.

How to edit Settings
------------------------

To edit settings, open the data folder, then edit the ``settings.yaml`` file as if it were a text (.txt) file.
If you want to know what each option does, go to the `Settings <settings.html>`_ page.
