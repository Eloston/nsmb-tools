# ClassID Tool
# Overlay patching library

import ovproc
import librom
import database

def create_patch(NewPatchPath, FromPatchDictionary, OVPath, Region):
    '''
    Write a patch based off the loaded Overlay and the original values from the PatchOriginal file
    '''
    iterate = 325
    while iterate > 0:
        modified = ovproc.ClassIDread(OVPath, iterate, Region)
        original = database.lookup(FromPatchDictionary, iterate)
        if modified != original:
            database.write_patch(NewPatchPath, iterate, modified)
        iterate = iterate - 1
    return 'Done'

def create_patch_rom(NewPatchPath, FromPatchDictionary, ROMPath, OVERLAYOffset):
    '''
    Write a patch based off the loaded Overlay and the original values from the PatchOriginal file
    '''
    iterate = 325
    while iterate > 0:
        modified = librom.ClassIDread(ROMPath, iterate, OVERLAYOffset)
        original = database.lookup(FromPatchDictionary, iterate)
        if modified != original:
            database.write_patch(NewPatchPath, iterate, modified)
        iterate = iterate - 1
    return 'Done'

def import_patch(Patch, Path, Region):
    '''
    Write a patch to an external Overlay0
    '''
    for Sprite in Patch.keys():
        ClassID = database.lookup(Patch, Sprite)
        ovproc.ClassIDwrite(Path, Sprite, Region, ClassID)
    return 'Done'

def import_patch_rom(Patch, Path, OVERLAYOffset):
    '''
    Import patch and write to an Overlay0 in the ROM
    '''
    for Sprite in Patch.keys():
        ClassID = database.lookup(Patch, Sprite)
        librom.ClassIDwrite(Path, Sprite, ClassID, OVERLAYOffset)
    return 'Done'
