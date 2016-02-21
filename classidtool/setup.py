# -*- coding: utf-8 -*-

'''
    This file is part of nsmb-tools.

    nsmb-tools is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    nsmb-tools is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with nsmb-tools. If not, see <http://www.gnu.org/licenses/>.
'''
# Simple distutils building script for the GUI interface

import sys
from cx_Freeze import setup, Executable

base = None
target_name = "ClassIDTool"
if sys.platform == 'win32':
    base = 'Win32GUI'
    target_name += ".exe"

directory_table = [ # https://msdn.microsoft.com/en-us/library/windows/desktop/aa368295(v=vs.85).aspx
    (
        "ProgramMenuFolder",
        "TARGETDIR",
        "."
    ),
    (
        "ClassIDToolProgramMenuFolder",
        "ProgramMenuFolder",
        "ClassID Tool"
    )
]

createfolder_table = [
    (
        "ClassIDToolProgramMenuFolder",
        "TARGETDIR"
    )
]

shortcut_table = [ # http://stackoverflow.com/questions/15734703/use-cx-freeze-to-create-an-msi-that-adds-a-shortcut-to-the-desktop
    (
        "AppShortcut",        # Shortcut
        "ClassIDToolProgramMenuFolder",          # Directory_
        "ClassID Tool",           # Name
        "TARGETDIR",              # Component_
        "[TARGETDIR]ClassIDTool.exe",# Target
        None,                     # Arguments
        None,                     # Description
        None,                     # Hotkey
        None,                     # Icon
        None,                     # IconIndex
        None,                     # ShowCmd
        'TARGETDIR'               # WkDir
    ),
    (
        "ResourcesDirShortcut",        # Shortcut
        "ClassIDToolProgramMenuFolder",          # Directory_
        "Open Resources Folder",           # Name
        "TARGETDIR",              # Component_
        "[TARGETDIR]resources",# Target
        None,                     # Arguments
        None,                     # Description
        None,                     # Hotkey
        None,                     # Icon
        None,                     # IconIndex
        None,                     # ShowCmd
        'TARGETDIR'               # WkDir
    )
]

removefile_table = [
    (
        "RemoveShortcutsFromFolder",
        "TARGETDIR",
        None,
        "ClassIDToolProgramMenuFolder",
        2
    )
]

property_table = [
    ("WhichUsers", "ALL")
]

options = {
    'build_exe': {
        'includes': 'atexit',
        'include_msvcr': True,
        'include_files': ["resources"]
    },
    'bdist_msi': {
        "add_to_path": False,
        "upgrade_code": "ClassIDTool",
        "data": { # https://msdn.microsoft.com/en-us/library/windows/desktop/aa368259(v=vs.85).aspx
            "Shortcut": shortcut_table,
            "Property": property_table,
            "Directory": directory_table,
            "CreateFolder": createfolder_table,
            "RemoveFile": removefile_table
        }
    }
}

executables = [
    Executable('main.py', base=base, targetName=target_name)
]

setup(name='ClassID Tool',
    version="6.1",
    description='Modify Sprite ID to Class ID mappings for NSMB ROMs',
    options=options,
    executables=executables
    )
