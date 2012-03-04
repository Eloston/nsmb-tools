ClassID Tool
============

Summary
-------

ClassID Tool is a tool to modify, read, and lookup names for Class IDs from a NSMB ROM or an extracted Overlay0 from a NSMB ROM. All NSMB ROM Regions are supported.

Requirements
------------

* Python 3.2.2
* PyQt4
* Overlay0 or NSMB ROM

Usage
-----

### Text-Interface
Double-click on txtinterface.py, or run 'python3 txtinterface.py'

### GUI
Double-click on guiinterface.py, or run 'python3 guiinterface.py'

Notes
-----
When reading/writing the Overlay0 in the ROM, make sure you have decompressed the Overlay0 (by pressing Decompress Overlay for the OV 0 item in the latest revisions of NSMBe), otherwise the tool will not be able to read/write ClassIDs.

You cannot read, or edit Sprite 0. For some reason, Sprite 0 will always crash the game, no matter the ClassID. You will get an error trying to read or edit Sprite 0

Contributing
------------
Please leave any problems, questions, or suggestions in the Issue Tracker

Credits
-------
Dirbaio
Treeki
Everyone else on the New Super Mario Bros. Hacking Domain.
