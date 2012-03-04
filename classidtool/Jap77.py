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
# Jap77 Module

def Decompress(data):
    '''
    Do Jap77 Decompression
    DATA is a byte object
    Port of SM64DSe's Jap77 Decompression with a slight change in decomp_len where size is added after doing the bitwise or and stuff
    '''
    data = bytearray(data)
    size = len(data)
    param1 = data[size - 8] | (data[size - 7] << 8) | (data[size - 6] << 16) | (data[size - 5] << 24)
    decomp_len = data[size - 4] | (data[size - 3] << 8) | (data[size - 2] << 16) | (data[size - 1] << 24)

    decomp_len = decomp_len + size

    inpos = size - (param1 >> 24) - 1
    limit = size - (param1 & 0x00FFFFFF)
    outpos = decomp_len - 1

    data = data + bytearray(decomp_len - size)
    while True:
        if inpos <= limit:
            break
        blockctl = data[inpos]
        inpos = inpos - 1
        if inpos <= limit:
            break
        done = False
        for i in range(8):
            if (blockctl & 0x80) == 0x80:
                if inpos <= limit:
                    done = True
                    break
                stuff = data[inpos - 1] | (data[inpos] << 8)
                inpos = inpos - 2
                wdisp = (stuff & 0x0FFF) + 2
                wsize = (stuff >> 12) + 2
                j = wsize
                while j >= 0:
                    data[outpos] = data[outpos + wdisp + 1]
                    outpos = outpos - 1
                    j = j - 1
            else:
                if inpos <= limit:
                    done = True
                    break
                data[outpos] = data[inpos]
                outpos = outpos - 1
                inpos = inpos - 1
            blockctl = blockctl << 1
        if done:
            return data
    return False
