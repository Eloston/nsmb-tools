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
# Parse NSMB ROM

import binascii
import libmisc
import ovproc
import mmap
import os.path

def check_header(ROMPath):
    '''
    Checks to see if the file is a NSMB ROM.
    If it is, then it will return True. Otherwise False
    '''
    HEADER = b'NEW MARIO'
    FILE =  open(ROMPath, mode='rb')
    BYTES = FILE.read(9)
    FILE.close()
    if BYTES == HEADER:
        return True
    else:
        return False

def detect_region(ROMPath):
    '''
    Return game region using the ROM header
    '''
    try:        
        ROM = open(ROMPath, mode='rb')
    except IOError:
        return 'Invalid ROM Path'
    ROM.seek(12)
    Char1 = chr(int(binascii.hexlify(ROM.read(1)), 16))
    Char2 = chr(int(binascii.hexlify(ROM.read(1)), 16))
    Char3 = chr(int(binascii.hexlify(ROM.read(1)), 16))
    Char4 = chr(int(binascii.hexlify(ROM.read(1)), 16))
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

def ReplaceOverlay(ROMPath, OverlayData):
    '''
    Replace the Overlay0 with the decompressed one
    '''
    ROM = open(ROMPath, mode='rb')
    # Get end of ROM location
    ROM.seek(128) #Go to location that defines the end of the ROM
    offpt4 = binascii.hexlify(ROM.read(1))
    offpt3 = binascii.hexlify(ROM.read(1))
    offpt2 = binascii.hexlify(ROM.read(1))
    offpt1 = binascii.hexlify(ROM.read(1))
    offset = b''.join([offpt1, offpt2, offpt3, offpt4]) #Finished reading offset to end of ROM
    # Define new Overlay position
    StartOverlay = int(offset, 16) + 136 # Define start of new overlay location. In new ROMs, the RSA sig starts where the header says the ROM ends.
    EndOverlay = StartOverlay + len(OverlayData) # Define end of new overlay location. It makes sense to subtract 1 because Startoverlay will become the first byte of the Overlay0, so subtracting 1 will make the offset point to the last byte. However, in the FAT table the end offset is one byte past the end of the file. So I shouldn't subtract 1
    # Check if ROM has enough space, and makes the ROM bigger if it isn't big enough
    ROM.close()
    if EndOverlay > os.path.getsize(ROMPath):
        ROM = open(ROMPath, mode='ab')
        ROM.write(bytes(EndOverlay - os.path.getsize(ROMPath)))
        ROM.close()
    ROM = open(ROMPath, mode='r+b')
    ROM = mmap.mmap(ROM.fileno(), 0)
    # Write Overlay to StartOverlay position of ROM
    ROM.seek(StartOverlay)
    ROM.write(bytes(OverlayData))
    # Change Overlay Table to say Overlay is already decompressed
    ROM.seek(int("50", 16)) #Go to place in header where Overlay Table offset is
    offpt4 = binascii.hexlify(ROM.read(1))
    offpt3 = binascii.hexlify(ROM.read(1))
    offpt2 = binascii.hexlify(ROM.read(1))
    offpt1 = binascii.hexlify(ROM.read(1))
    offset = b''.join([offpt1, offpt2, offpt3, offpt4])
    offset = int(offset, 16) #Finished getting table offset
    offset = offset + int("1F", 16) #Go to byte for Overlay0 that determins compressed or not
    ROM.seek(offset)
    CurrentValue = binascii.hexlify(ROM.read(1))
    ROM.seek(offset)
    CurrentValue = int(CurrentValue, 16) & 0xFE
    ROM.write_byte(CurrentValue) #Make last bit 0, which means it's already decompressed
    # Get FAT offset
    ROM.seek(72)
    offpt4 = binascii.hexlify(ROM.read(1))
    offpt3 = binascii.hexlify(ROM.read(1))
    offpt2 = binascii.hexlify(ROM.read(1))
    offpt1 = binascii.hexlify(ROM.read(1))
    offset = b''.join([offpt1, offpt2, offpt3, offpt4])
    FATOffset = int(offset, 16) #Finished getting FAT offset
    # NOTE: First FAT entry is Overlay0
    # Write start position of the Overlay0 to the FAT table
    ROM.seek(FATOffset)
    tmpoverlayoffset = (8 - len(hex(StartOverlay)[2:]))*'0' + hex(StartOverlay)[2:]
    ROM.write_byte(int(tmpoverlayoffset[6:], 16))
    ROM.write_byte(int(tmpoverlayoffset[4:6], 16))
    ROM.write_byte(int(tmpoverlayoffset[2:4], 16))
    ROM.write_byte(int(tmpoverlayoffset[:2], 16))
    # Write end position of the Overlay0 to the FAT table
    tmpoverlayoffset = (8 - len(hex(EndOverlay)[2:]))*'0' + hex(EndOverlay)[2:]
    ROM.write_byte(int(tmpoverlayoffset[6:], 16))
    ROM.write_byte(int(tmpoverlayoffset[4:6], 16))
    ROM.write_byte(int(tmpoverlayoffset[2:4], 16))
    ROM.write_byte(int(tmpoverlayoffset[:2], 16))
    # Update Header total ROM size
    ROM.seek(int("80", 16))
    ROM.write_byte(int(tmpoverlayoffset[6:], 16))
    ROM.write_byte(int(tmpoverlayoffset[4:6], 16))
    ROM.write_byte(int(tmpoverlayoffset[2:4], 16))
    ROM.write_byte(int(tmpoverlayoffset[:2], 16))
    # Compute CRC16 and update the header CRC
    ROM.seek(0)
    CRC = libmisc.CalcCRC16(ROM.read(350))
    ROM.seek(int("15E", 16))
    CRC = hex(CRC)[2:]
    ROM.write_byte(int(CRC[2:], 16))
    ROM.write_byte(int(CRC[:2], 16))
    # Wrap it up
    ROM.flush()
    ROM.close()

def DecompressOverlay0(ROMPath):
    '''
    Decompress the Overlay0 and insert the decompressed Overlay
    Use on new ROMs
    '''
    OverlayStart = get_overlay_offset(ROMPath, 0) # Easy way to get Overlay0 Offset
    ROM = open(ROMPath, mode='r+b')
    # Get FAT table offset
    ROM.seek(72)
    offpt4 = binascii.hexlify(ROM.read(1))
    offpt3 = binascii.hexlify(ROM.read(1))
    offpt2 = binascii.hexlify(ROM.read(1))
    offpt1 = binascii.hexlify(ROM.read(1))
    offset = b''.join([offpt1, offpt2, offpt3, offpt4])
    FATOffset = int(offset, 16) #Finished getting FAT offset
    # Get end of Overlay0 offset
    ROM.seek(FATOffset+4)
    offpt4 = binascii.hexlify(ROM.read(1))
    offpt3 = binascii.hexlify(ROM.read(1))
    offpt2 = binascii.hexlify(ROM.read(1))
    offpt1 = binascii.hexlify(ROM.read(1))
    offset = b''.join([offpt1, offpt2, offpt3, offpt4])
    OverlayEnd = int(offset, 16)
    ROM.seek(OverlayStart)
    OverlayData = ROM.read(OverlayEnd - OverlayStart)
    ROM.close()
    ReplaceOverlay(ROMPath, libmisc.OverlayDecompress(OverlayData))

def CheckOverlay0Decompressed(ROMPath):
    '''
    Check to see if the Overlay0 is already decompressed.
    Returns True if it is, returns False if it's not.
    '''
    ROM = open(ROMPath, mode='rb')
    ROM.seek(int("50", 16)) #Go to place in header where Overlay Table offset is
    offpt4 = binascii.hexlify(ROM.read(1))
    offpt3 = binascii.hexlify(ROM.read(1))
    offpt2 = binascii.hexlify(ROM.read(1))
    offpt1 = binascii.hexlify(ROM.read(1))
    offset = b''.join([offpt1, offpt2, offpt3, offpt4])
    offset = int(offset, 16) #Finished getting table offset
    offset = offset + int("1F", 16) #Go to byte for Overlay0 that determins compressed or not
    ROM.seek(offset)
    CurrentValue = int(binascii.hexlify(ROM.read(1)), 16)
    if CurrentValue % 2 == 0:
        return True
    else:
        return False
