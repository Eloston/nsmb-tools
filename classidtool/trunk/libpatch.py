# ClassID Tool
# Overlay patching library

import ovproc
import librom
import database
import mmap
import libmisc

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
    try:
        Overlay = open(Path, mode='r+b')
    except IOError:
        return 'Invalid Overlay Path'
    Overlay = mmap.mmap(Overlay.fileno(), 0)
    for Sprite in Patch.keys():
        ClassID = database.lookup(Patch, Sprite)
        if (libmisc.Spritenumchk(Sprite) != 'UNK') & (libmisc.ClassIDcheck(ClassID) != 'UNK'):
            ClassID = hex(ClassID)[2:]
            ZeroAdd = (4 - len(ClassID))*'0'
            ClassID = ''.join([ZeroAdd, ClassID])
            Overlay.seek(ovproc.ovoffset(Region) + Sprite*2 - 2)
            Overlay.write_byte(int(ClassID[2:], 16))
            Overlay.seek(ovproc.ovoffset(Region) + Sprite*2 - 1)
            Overlay.write_byte(int(ClassID[:2], 16))
        else:
            return "INVCLASSIDSPRITE"
    Overlay.flush()
    Overlay.close()
    return 'Done'

def import_patch_rom(Patch, Path, OVERLAYOffset):
    '''
    Import patch and write to an Overlay0 in the ROM
    '''
    try:
        ROM = open(Path, mode='r+b')
    except IOError:
        return 'Invalid ROM Path'
    ROM = mmap.mmap(ROM.fileno(), 20772366)
    for Sprite in Patch.keys():
        ClassID = database.lookup(Patch, Sprite)
        if (libmisc.Spritenumchk(Sprite) != 'UNK') & (libmisc.ClassIDcheck(ClassID) != 'UNK'):
            ClassID = hex(ClassID)[2:]
            ZeroAdd = (4 - len(ClassID))*'0'
            ClassID = ''.join([ZeroAdd, ClassID])
            ROM.seek(OVERLAYOffset + Sprite*2 - 2)
            ROM.write_byte(int(ClassID[2:], 16))
            ROM.seek(OVERLAYOffset + Sprite*2 - 1)
            ROM.write_byte(int(ClassID[:2], 16))
        else:
            return "INVCLASSIDSPRITE"
    ROM.flush()
    ROM.close()
    return 'Done'
