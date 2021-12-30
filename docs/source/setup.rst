Setup
=========
Now that installation is done, it's pretty much all a breeze from here on out. This section is a short one, first time
setup before you start to use STonitor.

Run STonitor
---------------
Run STonitor, to do so, open a command prompt window to STonitor's installation location (see Installation section if
you forgot how to do so) and enter ``python STonitor.py``. The program will open and notify you that there were missing
data files before exiting. You should now see a ``data`` folder in the root folder (if not, refresh file explorer).

Fill in Settings
-----------------
Open the ``data`` folder, inside it, you'll find a file named ``settings.yaml``. The majority of parameters will already
have a default value set, you can change them as needed to your preferences however.
`This documentation page <settings.html>`_ tells you what each of the parameters in the file mean. You can open this
file in most file editors, Notepad (or Notepad++ for the more advanced) will work perfectly fine.

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
Once you've adjusted all of the settings to your liking, STonitor is ready to go. To run it, simply navigate to the
folder in Command Prompt and enter ``python STonitor.py``. It's fairly straightforward but if you don't know how to
use it or want a refresher, head on over to `Usage <usage.html>`_.

Using a Batch file
---------------------
If you don't want to have to bother with command prompt everytime, you can also use a batch (.bat) file to run it.
Batch files basically run a sequence of command prompt commands automatically when you run it (if you're on Linux,
use bash, it's fairly similar and you probably already know how to). Using one is fairly easy, follow the below
instructions:

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
