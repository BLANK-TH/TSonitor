# STonitor
STonitor is an application  with the same general goal as MSWS' [Sonitor](https://github.com/MSWS/Sonitor) program, to 
facilitate admining eGO TTT & JB servers, by automatically analyzing logs outputted by those
servers. It can also show you the account age and CS:GO playtime (if available) of Steam accounts on the server.

*Do not rely solely on this program to determine whether something was an infraction, all analyses are done with only
the round logs as context. It can't possibly interpret anything that happened in game, it can only work with the 
information provided to it.*

## Documentation
Documentation on how to install, configure, and use STonitor is available on 
[Read the Docs](https://stonitor.blankdvth.com).

**Note**: Installing STonitor is not an easy task, mostly because I was too lazy to do it in a compiled language. If you
want a similar program that's much easier to install, use [Sonitor](https://github.com/MSWS/Sonitor).

## Features
A full feature list is available in the [documentation](ttps://stonitor.blankdvth.com), this is a quick summary. Most 
features and their sub-features can be disabled through a detailed settings file.

- Steam Age
  - Automatically runs when `status` in typed in the CS:GO console
  - Automatically retrieves and outputs the account age of everyone on the server
    - Steam accounts that are private has their age estimated by finding accounts created right after the private 
    account
  - Automatically retrieves and outputs their CS:GO playtime (if available)
  - Automatically retrieve and output their playtime on the server (if available)
- JB Log Analysis
  - Wardenless Freekill Detection
    - Tells you when a CT kills a non-rebelling T without a warden alive
  - New Warden Freekill Detection
    - Tells you when a CT kills a non-rebelling T within X seconds of a new warden coming on
  - Mass Freedamage Detection
    - Tells you when a CT hurts more than X people with utility (molotov or HE grenade) within Y seconds after throwing
    it
  - Early Vent Detection
    - Tells you when a CT breaks vents before any prisoners has
    - **Note**: On some maps, opening cell doors may count as breaking a vent, this is a false-positive, and I'll be 
    attempting to work on a fix in the near future
  - Button Grief Detection
    - Tells you when someone presses a button and players take damage from the world within X seconds
      - By default, Warden is not counted in this detection, it can be toggled off
    - Buttons can be ignored or renamed using the Button Configuration file
  - Nade Disruption Detection
    - Tells you when a prisoner throws utility and players take damage from the world within X seconds
  - Gunplant Detection
    - Tells you when a CT drops a weapon and a T uses that same weapon within X seconds
- TTT Log Analysis
  - RDM Detection
    - Tells you if there may have been a potential RDM (if enabled, can also go back and detect whether the RDM may have 
    been justified \[victim damaged the attacker first])
  - Mass RDM Detection
    - Tells you if a player has more than X bad kills (if enabled, can also detect reason for these kills)
  - Inno Utility Detection
    - Detects when an innocent damages someone with an HE grenade or molotov
- Log Summary Output
  - A summary of the logs that isn't as cluttered, what actions are shown in this summary can be configured
- Automatic Log Saving
  - Logs are automatically saved once they are received and parsed, so that you can always access them
