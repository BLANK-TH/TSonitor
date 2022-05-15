STonitor
====================================

Table of Contents
---------------------

.. toctree::
   :maxdepth: 1

   installation
   setup
   usage
   settings
   constants
   buttons
   changelog
   bugs
   faq

About
-------
STonitor is an application that's designed to help admins (and sometimes players) on eGO servers by automatically
analyzing TTT and JB logs to facilitate understanding them. STonitor also comes with a Steam Age feature which'll list
the age of steam accounts connected to any CS:GO server as well as CS:GO playtime (if available). This application may
eventually evolve to contain a broader spectrum of features that would be useful.

.. important:: This program is designed to assist in the analysis and understanding of logs, it cannot replace human
   discretion and understanding. This program is only able to make sense of the information provided to it (logs) and
   won't be able to understand what's going on in the game if it isn't in logs. An example would be the program
   reporting a JB wardenless freekill, the player that was supposedly freekilled is in armory and is thus KOS regardless
   of if there is a warden or not. The program is unable to tell because location information is unavailable in logs.

If you want to use this program, start with the step-by-step `Installation <installation.html>`_ instructions.

Features
---------
The majority of these features and their sub-features can be disabled using the detailed settings file. To understand
how to edit this file and what each parameter means, `go here <settings.html>`_.

* Steam Age
   * Automatically runs when ``status`` is typed in the CS:GO console
   * Automatically retrieves and outputs the account age of everyone on the server
      * If an account is private, the age is estimated by getting the ages of accounts created directly after the private account
   * Automatically retrieves and outputs player's CS:GO playtime if available
   * Automatically retrieves and outputs player's server playtime if available (using GameME)
* JB Log Analysis
   * **Wardenless Freekill**: *Notifies you when a CT kills a non-rebelling T without warden alive*
   * **New Warden Freekill**: *Notifies you when a CT kills a non-rebelling T within X seconds of a new warden coming on*
   * **ST Freekill**: *Notifies you when a CT kills an ST*
   * **Mass Freedamage**: *Notifies you when a CT throws an HE grenade or molotov and damages more than X Ts within Y seconds*
   * **Early Vent**: *Notifies you when a CT breaks a vent/wall before any T does*
      .. note:: On certain maps, a player opening cell doors may count as breaking a vent/wall, creating a false-positive
   * **Button Grief**: *Notifies you when someone presses a button and players take damage from the world within X seconds after*
      * By default, the warden is not counted in this, it can be toggled off in settings however
      * The damage threshold before a warning is triggered is configurable in settings
      * Buttons can be ignored or renamed using a Button Configuration file
   * **Nade Disruption**: *Notifies you when a prisoner throws utility and players take damage from the world within X seconds*
      * The damage threshold before a warning is triggered is configurable in settings
   * **Gunplant**: *Notifies you when a CT drops a weapon and a T uses that same weapon within X seconds*
* TTT Log Analysis
   * **RDM**: *Notifies you if there may have been a potential RDM*
      * The program can attempt to detect reasoning and eliminate reasonable bad kills. This is done by going back through logs to check if the 'victim' of the RDM attacked the potential RDMer first.
   * **Mass RDM**: *Notifies you if a player has more than X bad kills in a single round*
      * Similarly to RDM detection, Mass RDM detection can also attempt to detect reasoning, however this is disabled by default for Mass RDM
   * **Inno Utility**: *Notifies you when an innocent or detective damages someone with utility*
* **Log Summary Output**: *Creates a customizable summary of each round log, so that if you want to take a quick glance, its not as cluttered*
* **Automatic Log Saving**: *Automatically saves TTT & JB logs on your computer as .txt files, so that you can access them whenever*
   * TTT logs are saved in the format: ``TTT_round-number-here.txt`` with ``round-number-here`` being the TTT round number. E.g. ``TTT_12345.txt``
   * JB logs are saved in the format: ``JB_datetime-here.txt`` with ``datetime-here`` being the date and time down to the millisecond in which the log was initially processed. E.g. ``JB_Dec-28-2021_19-28-06_372498.txt``

Planned Features
-----------------
* Patch of cell opening false-positive for vent detection
* Button alias file support

Potential Features
--------------------
* Admin chat highlighting and storing
