# PyCoinach

Python port of [SaintCoinach](https://github.com/ufx/SaintCoinach/).

**This library currently only has support for extracting and converting SCD files to OGG (and FLAC).**

# CLI

```
usage: python -m pycoinach.cmd [-h] [-S] directory

Converts SCD files in a directory to OGG with loop metadata and FLAC that
loops twice.

positional arguments:
  directory      Directory containing SCD files.

optional arguments:
  -h, --help     show this help message and exit
  -S, --no-skip  Do not skip over SCD files that have corresponding OGG files
                 with the same name.
```

# How to extract SCD files from FFXIV

Download the latest [FFXIV File Explorer build](https://github.com/TheManii/FFXIV-Explorer/releases)
from their GitHub repo. The program itself requires JRE 8 to run, so go ahead, download and install that, too.

After you have downloaded and extracted the ZIP file to your computer, run `ffxiv explorer.jar`.

Set the path to your Final Fantasy XIV game directory by going to _Options > Settings_. Your Final Fantasy XIV
game directory contains the subdirectories `boot` and `game`.

Next go to _Tools_ then click _Find Music Hashes_.

## Finding SCD files

Open a `.index` file using _File > Open_, navigating to your game directory, then to _`game` > `sqpack`_.

 * `ffxiv` contains _A Realm Reborn_ and seasonal event data
 * `ex1` contains _Heavensward_ data
 * `ex2` contains _Stormblood_ data

Open each `.index` file to look for SCD files.

## Extracting SCD files

When you open a `.index` file containing a `music/` directory, click the `music/` in the left sidebar, then
go to `File` menu and then select `Save` (or <key>Ctrl</key>+<key>S</key>).

# Playing back OGG with loops

Download [playloop](https://github.com/jkarneges/playloop/releases).
