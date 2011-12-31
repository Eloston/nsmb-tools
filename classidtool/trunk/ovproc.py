# ClassID Tool
# Overlay Processor

import binascii
import mmap

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

def Spritenumchk(Sprite):
    '''    
    Check to make sure the Sprite number is valid
    '''    
    if 1 <= Sprite <= 323:
        return Sprite
    else:
        return 'UNK'

def ClassIDcheck(ClassID):
    '''
    Check to make sure the ClassID value is valid
    '''
    if 0 <= ClassID <= 65536:
        return ClassID
    else:
        return 'UNK'

def ClassIDread(OVPath, Sprite, Region):
    '''    
    Read the ClassID of a specific Sprite and return a decimal representation of it
    '''    
    if Spritenumchk(Sprite) != 'UNK':
        Overlay = open(OVPath, mode='rb')
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
    if (Spritenumchk(Sprite) != 'UNK') & (ClassIDcheck(ClassID) != 'UNK'):
        ClassID = hex(ClassID)[2:]
        ZeroAdd = (4 - len(ClassID))*'0'
        ClassID = ''.join([ZeroAdd, ClassID])
        Overlay = open(OVPath, mode='r+b')
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
