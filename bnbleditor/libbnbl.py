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
# bnbl editing/reading library

import mmap
import binascii

def verify_bnbl_header(bnblFile):
    '''
    Return True if bnbl header is correct, otherwise return False
    '''
    bnblFile.seek(0)
    Char1 = str(bnblFile.read(1))[2:][:1]
    Char2 = str(bnblFile.read(1))[2:][:1]
    Char3 = str(bnblFile.read(1))[2:][:1]
    Char4 = str(bnblFile.read(1))[2:][:1]
    bnblheader = ''.join([Char1, Char2, Char3, Char4])
    if bnblheader.upper() == "JNBL":
        return True
    else:
        return False

def num_touchregions(bnblFile, Value):
    '''
    Check the number of touch regions or change the value
    '''
    bnblFile.seek(6)
    if Value[0]:
        HexValue = str(hex(Value[1]))[2:]
        ZeroAdd = (4 - len(HexValue))*'0'
        WriteValue = ''.join([ZeroAdd, HexValue])
        bnblFile.write_byte(int(WriteValue[2:], 16))
        bnblFile.write_byte(int(WriteValue[:2], 16))

    else:
        Small = str(binascii.hexlify(bnblFile.read(1)))[2:][:2]
        Big = str(binascii.hexlify(bnblFile.read(1)))[2:][:2]
        TouchRegions = int(''.join([Big, Small]), 16)
        return TouchRegions - 1

def touchregions(bnblFile, Value):
    '''
    Read the values of a touch region, or write values
    '''
    bnblFile.seek(8+Value[1]*6)
    if Value[0]:
        for ATTRIBUTE in Value[2]:
            if not ATTRIBUTE == None:
                bnblFile.write_byte(ATTRIBUTE)
    else:
        XCORD1 = int(str(binascii.hexlify(bnblFile.read(1)))[2:][:2], 16)
        XCORD2 = int(str(binascii.hexlify(bnblFile.read(1)))[2:][:2], 16)
        XCORD = XCORD1 - XCORD2
        YCORD1 = int(str(binascii.hexlify(bnblFile.read(1)))[2:][:2], 16)
        YCORD2 = int(str(binascii.hexlify(bnblFile.read(1)))[2:][:2], 16)
        YCORD = YCORD1 - YCORD2
        WIDTH = int(str(binascii.hexlify(bnblFile.read(1)))[2:][:2], 16)
        HEIGHT = int(str(binascii.hexlify(bnblFile.read(1)))[2:][:2], 16)
        return [XCORD, YCORD, WIDTH, HEIGHT]

def addremove_touchregions(bnblFile, Value):
    if Value[0]:
        bnblFile.resize(bnblFile.size() + 6*Value[1])
        num_touchregions(bnblFile, [True, num_touchregions(bnblFile, [False])+1+Value[1]])
    else:
        bnblSize = bnblFile.size()
        NewValue = Value[1] + 1
        bnblFile.move(8+NewValue*6-6, 8+NewValue*6, bnblSize - (8+NewValue*6))
        bnblFile.resize(bnblSize-6)
        num_touchregions(bnblFile, [True, num_touchregions(bnblFile, [False])])

def repairbnbl(bnblFile, TYPE):
    '''
    Repairs a bnbl file.
    if Type is True, then the file will shrink or expand by the index value
    otherwise, the index will be updated by the number of touchregions
    '''
    if TYPE:
        INDEX = num_touchregions(bnblFile, [False]) + 1
        bnblFile.resize(8+INDEX*6)
    else:
        bnblSize = bnblFile.size()
        TouchRegionNum = (bnblSize-8)/6
        if str(type(TouchRegionNum)) == "<class 'float'>":
            TouchRegionNum = int(TouchRegionNum) + 1
        bnblFile.resize(8+TouchRegionNum*6)
        num_touchregions(bnblFile, [True, TouchRegionNum])

def compute_xy_cord(Value):
    return [Value, 0]
