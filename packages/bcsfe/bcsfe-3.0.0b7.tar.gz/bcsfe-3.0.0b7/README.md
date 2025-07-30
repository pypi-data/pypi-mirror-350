# Battle Cats Save File Editor

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/M4M53M4MN)

BCSFE is a python command line save editor for The Battle Cats.

Join the [discord server](https://discord.gg/DvmMgvn5ZB) if you want to suggest
new features, report bugs or get help on how to use the editor (please read the
below tutorials / watch the latest
[tutorial video](https://www.youtube.com/watch?v=Kr6VaLTXOSY) first before
asking for help).

## Thanks to

Lethal's editor for giving me inspiration to start the project and it helped me
work out how to patch the save data and edit cf/xp: <https://www.reddit.com/r/BattleCatsCheats/comments/djehhn/editoren/>

Beeven and csehydrogen's open source code, which helped me figure out how to
patch save data: [beeven/battlecats](https://github.com/beeven/battlecats), [csehydrogen/BattleCatsHacker](https://github.com/csehydrogen/BattleCatsHacker)

Everyone who's given me saves, which helped to test save loading/saving and to
test/develop new features

## How to use

If you have a pc: watch a [Tutorial video](https://www.youtube.com/watch?v=Kr6VaLTXOSY),
or scroll down for a text tutorial

If you only have an android device: read the [Android text tutorial](#android-tutorial)

If you only have an ios device: watch the [IOS tutorial
video](https://www.youtube.com/watch?v=xw-uOqQRYJ8) (Made by Viarules, NOTE:
Some people have said that ish is really slow, and you should use a-shell
instead)

## Main tutorial

1. Install python (You'll need version 3.9 and up) <https://www.python.org/downloads/>

1. Follow the `Install from source` instructions below as 3.0.0 isn't on pypi
   yet

1. Enter the command: `py -m bcsfe` to run the editor. If that doesn't work
then use `python3` or `python` instead of `py` in the command

1. Go into the in-game transfer system in `Settings-> Data Transfer` and
click `Begin Data Transfer`

1. In the editor use the option called `Download save file using transfer and
confirmation code` (enter the corresponding number, not the name itself)

1. Enter your transfer code

1. Enter your confirmation code

1. Select the country code that you are using, `en`=english,
`kr`=korean, `jp`=japanese, `tw`=taiwanese.

1. Edit what you want. Note that in most cases, if you want to exit the current
   input you can enter `q` and press enter to go back to the previous menu

1. Go into the `Save Management` option and select `Save changes and upload to
game servers (get transfer and confirmation codes)`. It may take some time, it
may also fail, if it does then try again

1. Enter those codes into the game's transfer system (click on
`Resume Data Transfer`) (You may need to `Cancel Data Transfer`
in-game before doing so)

### Using a rooted device via adb

1. Add adb to your PATH environment variable, or edit the config to set ADB path
  to the full path of the adb executable. You can download adb from
  [adb](https://developer.android.com/studio/releases/platform-tools)

1. Open the editor and select the option named `Pull save file from device
using adb` and enter your game version, or select the option named
`Select save file from file` and select a copy of your save data

1. Edit what you want

1. Go into save management and select an option to push save data to the game

1. Enter the game and you should see changes

### Using a rooted device directly

1. You need to be running the editor on the device itself, so you'll need to
follow the [Android tutorial](#android-tutorial) to install the editor

1. Open the editor and select the option named `Pull save file from root
   storage`

1. Edit what you want

1. Go into save management and select an option to push save data to the game

1. Enter the game and you should see changes

### How to unban your account

1. Select the option in `Account` to `Unban account` or
just upload the save data to the game servers again

1. It may take some time but after, you should be able to choose one of the
options in save management to push the save data to the game.

#### How to prevent a ban in the future

- Instead of editing in platinum tickets use the `Platinum Shards` feature

- Instead of editing in rare tickets use the `Normal Ticket Max Trade Progress
(allows for unbannable rare tickets)` feature

- Instead of hacking in cat food, just edit everything in that you can buy with
cat food, e.g battle items, catamins, xp, energy refills (leaderships), etc.
If you really want catfood then you can clear and unclear catnip missions with
the feature `Catnip Challenges / Missions` then entering 1 when asked.
You'll need to collect the catfood in-game after each clear though

- Instead of hacking in tickets, just hack in the cats/upgrades you want directly

## Android Tutorial

If you don't have a pc to install and run the editor you can use Termux.

1. Download [F-Droid](https://f-droid.org/F-Droid.apk) - You can download the
Termux apk directly but then it won't automatically update. You cannot
download Termux from the Play Store because it does not work

1. Install F-Droid

1. Open it and wait for it to finish `Updating repositories`

1. Tap the green search button in the bottom right and search for `Termux`

1. Tap `Termux Terminal emulator with packages`

1. Tap `INSTALL` and then `OPEN` once installed

1. Once opened enter the command `pkg install python`

1. If that doesn't work then read this: <https://stackoverflow.com/a/71097459>

1. Then follow the `Install from source` instructions below

1. If that doesn't work then run `pkg upgrade` and try again

1. Then run `python -m bcsfe`

1. Note that the editor might complain about not being to run tkinter, but you
can ignore that and just enter `SAVE_DATA` when asked to enter the path to a
save file

1. You can then use the editor like normal

### Install from source

If you want the latest features then you can install the editor from the github.

1. Download [Git](https://git-scm.com/downloads)

2. Run the following commands: (You may have to replace `py` with `python` or `python3`)

```batch
git clone https://github.com/fieryhenry/BCSFE-Python.git
cd BCSFE-Python
git checkout 3.0.0
pip install -e .
py -m bcsfe
```

If you want to use the editor again all you need to do is run the `py -m bcsfe` command

Then if you want the latest changes you only need to run `git pull` in the downloaded
`BCSFE-Python` folder. (use `cd` to change the folder)

## Documentation

- [Custom Locales](https://github.com/fieryhenry/ExampleEditorLocale)
- [Custom Themes](https://github.com/fieryhenry/ExampleEditorTheme)

I only have documentation for the locales and themes atm, but I will probably
add more documentation in the future.
