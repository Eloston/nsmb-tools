# ClassID Tool
# Overlay Processor

import binascii

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

def byteread(OVPath, Sprite, Region):
    '''    
    Read the ClassID of a specific Sprite and return a decimal representation of it
    '''    
    Overlay = open(OVPath, mode='rb')
    if Spritenumchk(Sprite) != 'UNK':
        Overlay.seek(ovoffset(Region) + Sprite*2 - 2)
    else:
        Overlay.close()
        return 'INVSPRITE'
    Byte2 = binascii.hexlify(Overlay.read(1))
    Byte1 = binascii.hexlify(Overlay.read(1))
    Overlay.close()  
    Value = b''.join([Byte1, Byte2])
    Value = int(Value, 16)
    return Value
