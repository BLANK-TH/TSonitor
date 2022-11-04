Setup
=========
Now that installation is done, it's pretty much all a breeze from here on out. This section is a short one, first time
setup before you start to use STonitor.

Configure CS:GO AutoExec
--------------------------
By default, CS:GO doesn't output it's console anywhere, in order for this program to work, we need to change that.
Luckily it's pretty simple!

1. Open up a file explorer window and navigate to your CS:GO cfg directory, for most people, it's at: ``C:/Program Files (x86)/Steam/steamapps/common/Counter-Strike: Global Offensive/csgo/cfg``.
2. In that folder, open the file named ``autoexec.cfg`` (if this file doesn't exist, that's fine, create one that's named that exactly)
3. Near the end of the file, add this line in: ``con_logfile output.log``
4. Save the file
5. Run CS:GO once so that the file gets generated (STonitor checks if it exists before running)

Run STonitor
---------------
Run STonitor, how this is done depends on how you installed it. If you installed STonitor via the Installer, simply
double-click the Desktop Shortcut, or find it in the run menu (the same way you do any other program).

If you performed a manual installation, open a command prompt window to STonitor's installation location (see the
Installation section if you forgot how to do so) and enter ``python STonitor.py``.

The program will open and notify you that there were missing data files and that it created them. This is normal for
first time setup. It will also ask you whether you want to open the data folder, enter ``Y``, then press enter.

Fill in Settings
-----------------
Open the ``data`` folder (the program should have automatically opened it for you if you asked it to, if you didn't,
see the FAQ entry on the `location of the data folder <faq.html#where-is-the-data-folder>`_). Inside this data folder,
you'll find a file named ``settings.yaml``. The majority of parameters will already have a default value set, you can
change them as needed to your preferences however. `This documentation page <settings.html>`_ tells you what each of
the parameters in the file mean. You can open this file in most file editors, Notepad (or Notepad++ for the more
advanced) will work perfectly fine.

Fill in the Steam API Key
---------------------------
In ``settings.yaml`` you'll find an empty parameter named ``steamkey``. If you want to use the steam account age
(and/or CS:GO playtime) feature, you'll need to fill this in. A steam API key is what is used to authenticate with
Steam in order to retrieve this data. Luckily getting one is a piece of cake, head on over to
`this steam page <https://steamcommunity.com/dev/apikey>`_ and you can easily get one (you will need to login). Once
you've gotten one, paste it into the file. It should look something like this: ``steamkey: '31312ANDSAHW1324'`` (actual
steamkey in the example is made up, yours will likely be longer and look different).

All Set
---------
Once you've adjusted all of the settings to your liking, STonitor is ready to go. To run it, simply double-click the
desktop shortcut (if you used the Installer), or navigate to the folder in Command Prompt and enter
``python STonitor.py`` (if you performed a manual installation).

It's fairly straightforward to use, but if you don't know how to use it or want a refresher, head on over to `Usage <usage.html>`_.

Using a Batch File (only for manual installation)
---------------------
If you performed a manual installation and don't want to have to bother with command prompt everytime, you can also
use a batch (.bat) file to run it. Batch files basically run a sequence of command prompt commands automatically when
you run it (if you're on Linux, use bash, it's fairly similar and you probably already know how to). Using one is
fairly easy, follow the below instructions:

1. Find the location want the Batch file to be. Right click, hover over new, then click Text Document.
2. When it asks you for a name (this step is important), press Ctrl + A (select all text), and enter ``STonitor.bat``. It doesn't have to start with STonitor, it can be whatever you like as long as it ends with ``.bat``.
3. It'll tell you that changing a file's extension can make it unusable, it'll be perfectly fine, click Yes.
4. Right click the file that it's created, then click Edit
5. Paste the following code into the file and save it, replace the path in the example with the full path to where you installed STonitor.

.. code-block:: bash

    @echo off
    cls
    title STonitor
    cd C:/Users/Username/Desktop/STonitor
    python STonitor.py
    pause

.. hint:: You can also move this file to your Home directory (this is usually ``C:\Users\Username\``) so that you can
    just enter the filename of the bat file in Run (Windows + R) to access it easier. E.g. if your filename is
    ``stonitor.bat``, you can just enter ``stonitor`` in Run for it to open.
