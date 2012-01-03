# ClassID Tool
# Overlay patching library

import ovproc
import database

def create_patch(NewPatchPath, FromPatchDictionary, OVPath, Region):
    iterate = 325
    while iterate > 0:
        modified = ovproc.ClassIDread(OVPath, iterate, Region)
        original = database.lookup(FromPatchDictionary, iterate)
        if modified != original:
            database.write_patch(NewPatchPath, iterate, modified)
        iterate = iterate - 1
    return 'Done'

def import_patch(Patch, OVPath, Region):
    for Sprite in Patch.keys():
        ClassID = database.lookup(Patch, Sprite)
        ovproc.ClassIDwrite(OVPath, Sprite, Region, ClassID)
    return 'Done'
