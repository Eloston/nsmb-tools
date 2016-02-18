ClassID Tool
============

Summary
-------
ClassID Tool is a tool to modify, read, and lookup names for Class IDs from a NSMB ROM or an extracted Overlay0 from a NSMB ROM. All NSMB ROM Regions are supported.

Requirements
------------
* Python 3
* PyQt4
* Overlay0 or NSMB ROM

Usage
-----
1. Run `main.py` or the main executable
2. Go to `File -> Open` and select the NSMB ROM or Overlay0 file

### Patches
Patches define the mapping of Sprite IDs to Class IDs. They are text files containing entries delimited by newlines. During application, only the Sprite IDs present in the patch will be modified; the rest will be left untouched.

The format of an entry is as follows:
```
{sprite_id#class_id)
```
Where `sprite_id` is substituted with the Sprite ID, and `class_id` is substituted with the Class ID.

### NameDatabase file
This file defines the names for the Class IDs. It is a text file with multiple entries.

Each entry has the following format:
```
{class_id#name}
```
Where `class_id` is the Class ID, and `name` is the corresponding name. Blank lines and lines lines starting with `#` are ignored.

### Notes
When reading/writing the Overlay0 in the ROM, make sure you have decompressed the Overlay0 (by pressing Decompress Overlay for the OV 0 item in the latest revisions of NSMBe), otherwise the tool will not be able to read/write ClassIDs.

You cannot read, or edit Sprite 0. For some reason, Sprite 0 will always crash the game, no matter the ClassID. You will get an error trying to read or edit Sprite 0

Generating Portable Binaries
----------------------------
See [BUILDING](BUILDING.md)

Contributing
------------
Please leave any problems, questions, or suggestions in the Issue Tracker

Credits
-------
Dirbaio
Treeki
Everyone else on the New Super Mario Bros. Hacking Domain.
