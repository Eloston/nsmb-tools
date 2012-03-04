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
def write_patch(PatchPath, Sprite, ClassID):
    with open(PatchPath, mode='a') as Patch:
        Patch.write(''.join(['{', str(Sprite), '#', str(ClassID), '}', '\n']))

def start(PatchPath):
    iterable = 325
    while iterable > 0:
        write_patch(PatchPath, iterable, iterable)
        iterable = iterable - 1
    return 'Done'
start(input("Put in path to generate patch"))
