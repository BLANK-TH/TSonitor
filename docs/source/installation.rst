Installation
==============

There are two ways to install STonitor, you can use the provided Installer for Windows, or you can install it manually.
The Installer is not guaranteed to work, and may potentially cause a false-positive in your antivirus software.
If you are concerned about this, you can install it manually.

Installer
---------

As of version 2.2.0, STonitor has an installer for Windows. This is the easiest way to install STonitor,
although less stable than the manual installation (if you know what you're doing when performing the manual
installation).

Downloading the Installer
^^^^^^^^^^^^^^^^^^^^^^^^^

1. Head over to the releases page and grab the latest version. This `link <https://github.com/blankdvth/STonitor/releases/latest>`_ also brings you there.
2. Once you've found a proper release, check the assets section near the bottom and download the Installer (``STonitor_Setup_X.X.X.exe``, the Xs are version numbers).

Running the Installer
^^^^^^^^^^^^^^^^^^^^^

Once you have the Installer downloaded, you'll need to run it. In order to do this, head over to the location where you
downloaded the Installer, and double-click it. Windows SmartScreen may pop up, warning you about the Installer being
potentially unsafe, this is because the Installer is not signed. You can safely ignore this warning and continue with
the installation by clicking ``More info``, then ``Run Anyway``.

Continue through the installation process, and you should be good to go! Once the installation is complete, you can
get started on the `Setup <setup.html>`_.

Manual Installation
-------------------

STonitor's manual installation is neither streamlined or easy, depending on how experienced you are with things like
this, things may go wrong (solutions to some common issues may be available in the `FAQ <faq.html>`_). If you want
something easy to install, you can use the :ref:`Installer<Installer>` or check out
`Sonitor <https://github.com/MSWS/Sonitor>`_ by *MSWS*.

Emphasis and warnings aside, the installation instructions below are fairly detailed, as long as you follow them, you
should be fine. This installation process is also fairly standard, if you encounter an issue not covered in the FAQ,
you'll likely be able to find a solution fairly fast by Googling it.

Installing Python
^^^^^^^^^^^^^^^^^
STonitor is made using Python, and needs Python to run. If you've already installed a 3.X version, great, you can skip
this part. If not, follow the steps below:

1. Download a 3.X version of Python, to do so, head to `Python's official site <https://www.python.org/downloads/>`_. Don't install the version on the Microsoft Store, that commonly causes odd problems.
    .. note:: This program was developed on the 3.8.2 version, however the majority of modern v3.X versions should all
        work fine
2. Run the installer (may differ depending on Operating System).
    .. attention:: Be on the lookout for a checkbox labeled ``Add to PATH`` while installing, make sure that it's
        checked or you'll likely run into issues.
3. Once the installation has been completed, test it. Open up a command prompt window and type ``python --version``.
    * If the version number you installed pops up, it's installed properly, congrats!
    * If the command is unrecognized, make sure that it's installed properly **AND** added to PATH.
    * If the version number is wrong, you may already have a version installed, as long as it's 3.X, you can use it.

Downloading STonitor
^^^^^^^^^^^^^^^^^^^^
Congrats on installing Python. The next part is fairly straightforward, download the most recent version of STonitor.

1. Head over to the releases page and grab the latest version. This `link <https://github.com/blankdvth/STonitor/releases/latest>`_ also brings you there.
2. Once you've found a proper release, check the assets section near the bottom and download the one labeled ``Source code (zip)``.
3. When the download has finished, extract the ZIP file to your location of choice. This is where the program will reside, so it's recommended not to leave it in Downloads and rather someplace accessible and memorable.

Installing Requirements
^^^^^^^^^^^^^^^^^^^^^^^
That was easy, wasn't it? This one's slightly harder, but still not horrible. We're going to be installing the packages
(requirements) that are needed for STonitor to operate properly.

1. Open up a command prompt window and navigate to the folder where you installed STonitor. There are multiple ways of doing this, here's the most common two:
    * This is the fastest way. Open up Windows Explorer to where you extracted STonitor, then click the address bar (the thing at the top that shows where you are) and enter ``cmd`` then press enter. This will automatically open up command prompt to the proper location
    * This is another slower way if the first one doesn't work out. Press Windows + R, and enter ``cmd`` in the Run dialog. Press enter and it'll open Command Prompt, after that, cd (change directory) to where you installed STonitor. To do so, enter ``cd path/to/stonitor/here``, replacing ``path/to/stonitor/here`` with the path to STonitor's install location
2. Once you've opened up a command prompt window and properly navigated to STonitor's install location (make sure you're in the root folder, that's the folder that has the file named ``requirements.txt``), enter the following command: ``pip install -r requirements.txt``. You should see an output and multiple progress bars installing the packages.
    .. tip:: If it says command not found, first try to replace ``pip`` with ``pip3``. If it still doesn't work, try to replace it with ``python -m pip``. If it still doesn't work, go back and make sure you installed Python properly.
    .. tip:: If it says that it couldn't find ``requirements.txt``, make sure you're in the right folder
3. Make sure that everything has been properly installed (you should see ``Successfully installed`` then a lot of names)

Done
^^^^
Congrats! You've finished the installation portion, now get started on the `Setup <setup.html>`_.
