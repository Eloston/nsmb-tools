# ClassID Tool
# File Updating Library

import urllib.request
import liburllist

def NameDatabase(PATH, URLListDict):
    '''
    Update NameDatabase file
    '''
    try:
        NSMBHD_HTTP = urllib.request.urlopen(liburllist.lookup(URLListDict, "NSMBHD_NameDB"))
        NSMBHD = NSMBHD_HTTP.read()
        NSMBHD_HTTP.close()
    except:
        return "NSMBHD_FAILED"
    try:
        Unused_HTTP = urllib.request.urlopen(liburllist.lookup(URLListDict, "Unused_NameDB"))
        Unused = Unused_HTTP.read()
        Unused_HTTP.close()
    except:
        return "Unused_FAILED"
    UpdatedDB = b'# Unused ClassIDs\n'.join([NSMBHD, Unused])
    try:
        NameDB = open(PATH, mode='wb')
    except:
        return "Open_FAILED"
    NameDB.write(UpdatedDB)
    NameDB.close()
    return "Sucess"
