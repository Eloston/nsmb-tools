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
