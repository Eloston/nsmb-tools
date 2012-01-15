# ClassID Tool
# Parse NSMB ROM

import binascii
import libmisc
import ovproc
import mmap
import os.path

def detect_region(ROMPath):
    '''
    Return game region using the ROM header
    '''
    try:        
        ROM = open(ROMPath, mode='rb')
    except IOError:
        return 'Invalid ROM Path'
    ROM.seek(12)
    Char1 = hex(int(ROM.read(1), 16))[2:]
    Char2 = hex(int(ROM.read(1), 16))[2:]
    Char3 = hex(int(ROM.read(1), 16))[2:]
    Char4 = hex(int(ROM.read(1), 16))[2:]
    ROM.close()
    Gamecode = ''.join([Char1, Char2, Char3, Char4])
    if Gamecode.upper() == 'A2DE':
        return 'USA'
    elif Gamecode.upper() == 'A2DP':
        return 'EUR'
    elif Gamecode.upper() == 'A2DJ':
        return 'JAP'
    elif Gamecode.upper() == 'A2DK':
        return 'KOR'
    else:
        return 'UNK'

def get_overlay_offset(ROMPath, OVERLAYOffset):
    '''
    Get decimal representation of the offset of the Overlay0 from the ROM
    '''
    try:        
        ROM = open(ROMPath, mode='rb')
    except IOError:
        return 'Invalid ROM Path'
    ROM.seek(72)
    offpt4 = binascii.hexlify(ROM.read(1))
    offpt3 = binascii.hexlify(ROM.read(1))
    offpt2 = binascii.hexlify(ROM.read(1))
    offpt1 = binascii.hexlify(ROM.read(1))
    offset = b''.join([offpt1, offpt2, offpt3, offpt4])
    offset = int(offset, 16)
    ROM.seek(offset)
    offpt4 = binascii.hexlify(ROM.read(1))
    offpt3 = binascii.hexlify(ROM.read(1))
    offpt2 = binascii.hexlify(ROM.read(1))
    offpt1 = binascii.hexlify(ROM.read(1))
    offset = b''.join([offpt1, offpt2, offpt3, offpt4])
    offset = int(offset, 16)
    ROM.close()
    return offset+OVERLAYOffset

def ClassIDread(ROMPath, Sprite, OVERLAYOffset):
    '''
    Read the Class ID from the Overlay 0 from the ROM
    '''
    if libmisc.Spritenumchk(Sprite) != 'UNK':
        try:        
            ROM = open(ROMPath, mode='rb')
        except IOError:
            return 'Invalid ROM Path'
        ROM.seek(OVERLAYOffset + Sprite*2 - 2)
        Byte2 = binascii.hexlify(ROM.read(1))
        Byte1 = binascii.hexlify(ROM.read(1))
        ROM.close()  
        Value = b''.join([Byte1, Byte2])
        Value = int(Value, 16)
        return Value
    else:
        return 'INVSPRITE'

def ClassIDwrite(ROMPath, Sprite, ClassID, OVERLAYOffset):
    '''
    Write the decimal representation of a ClassID for a sprite to the ROM
    '''
    if (libmisc.Spritenumchk(Sprite) != 'UNK') & (libmisc.ClassIDcheck(ClassID) != 'UNK'):
        ClassID = hex(ClassID)[2:]
        ZeroAdd = (4 - len(ClassID))*'0'
        ClassID = ''.join([ZeroAdd, ClassID])
        try:
            ROM = open(ROMPath, mode='r+b')
        except IOError:
            return 'Invalid ROM Path'
        ROM = mmap.mmap(ROM.fileno(), 20772366)
        ROM.seek(OVERLAYOffset + Sprite*2 - 2)
        ROM.write_byte(int(ClassID[2:], 16))
        ROM.seek(OVERLAYOffset + Sprite*2 - 1)
        ROM.write_byte(int(ClassID[:2], 16))
        ROM.flush()
        ROM.close()
        return "Done"
    else:
        return "INVCLASSIDSPRITE"
