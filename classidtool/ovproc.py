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
# Overlay Processor

import binascii
import mmap
import libmisc

def check_header(OVPath):
    '''
    Check the header of the Overlay to see if it's valid.
    Returns True if header is valid, otherwise returns False
    '''
    HEADER = b'10402de9'
    FILE = open(OVPath, mode='rb')
    BYTES = binascii.hexlify(FILE.read(4))
    FILE.close()
    if BYTES == HEADER:
        return True
    else:
        return False

def ovoffset(Region):
    '''
    Returns the decimal offset for Sprite 1's ClassID
    '''
    if Region == 'USA':
        return 170970
    elif Region == 'EUR':
        return 168134
    elif Region == 'JAP':
        return 167946
    elif Region == 'KOR':
        return 168162

def region_detect(OVPath):
    with open(OVPath, mode='rb') as Overlay:
        Overlay.seek(28)
        Byte = Overlay.read(1)
        Overlay.close()
        if Byte == b'\x84':
            return 'USA'
        elif Byte == b'\x64':
            return 'EUR'
        elif Byte == b'\x04':
            return 'JAP'
        elif Byte == b'\xC4':
            return 'KOR'
        else:
            return 'UNK'

def ClassIDread(OVPath, Sprite, Region):
    '''    
    Read the ClassID of a specific Sprite and return a decimal representation of it
    '''    
    if libmisc.Spritenumchk(Sprite) != 'UNK':
        try:        
            Overlay = open(OVPath, mode='rb')
        except IOError:
            return 'Invalid Overlay Path'
        Overlay.seek(ovoffset(Region) + Sprite*2 - 2)
        Byte2 = binascii.hexlify(Overlay.read(1))
        Byte1 = binascii.hexlify(Overlay.read(1))
        Overlay.close()  
        Value = b''.join([Byte1, Byte2])
        Value = int(Value, 16)
        return Value
    else:
        return 'INVSPRITE'

def ClassIDwrite(OVPath, Sprite, Region, ClassID):
    '''
    Write the decimal representation of a ClassID for a sprite to the overlay
    '''
    if (libmisc.Spritenumchk(Sprite) != 'UNK') & (libmisc.ClassIDcheck(ClassID) != 'UNK'):
        ClassID = hex(ClassID)[2:]
        ZeroAdd = (4 - len(ClassID))*'0'
        ClassID = ''.join([ZeroAdd, ClassID])
        try:
            Overlay = open(OVPath, mode='r+b')
        except IOError:
            return 'Invalid Overlay Path'
        Overlay = mmap.mmap(Overlay.fileno(), 0)
        Overlay.seek(ovoffset(Region) + Sprite*2 - 2)
        Overlay.write_byte(int(ClassID[2:], 16))
        Overlay.seek(ovoffset(Region) + Sprite*2 - 1)
        Overlay.write_byte(int(ClassID[:2], 16))
        Overlay.flush()
        Overlay.close()
        return "Done"
    else:
        return "INVCLASSIDSPRITE"
