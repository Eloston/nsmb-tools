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
# Name and Patch Database parsing module

import libmisc
import re

def readdb(NameDB):
    '''
    Import Name Database and return a dictionary
    '''
    regexp = re.compile(r"\{(?P<ClassID>[0-9]+)\#(?P<Name>.+)\}")
    db = dict()
    with open(NameDB, mode='r') as Database:
        for line in Database:
            m = regexp.match(line)
            if not m == None:
                db[int(m.group('ClassID'))] = m.group('Name')

    return db

def lookup(db, value):
    '''
    Lookup name or classid in Name or Patch Database dictionary
    '''
    try:
        return db[value]
    except KeyError:
        return "INVVALUE"

def read_patch(PatchDB):
    '''
    Import Patch Database and return a dictionary
    '''
    regexp = re.compile(r"\{(?P<Sprite>[0-9]+)\#(?P<ClassID>[0-9]+)\}")
    db = dict()
    with open(PatchDB, mode='r') as Database:
        for line in Database:
            m = regexp.match(line)
            if not m == None:
                db[int(m.group('Sprite'))] = int(m.group('ClassID'))

    return db

def write_patch(PatchPath, Sprite, ClassID):
    '''
    Write a patch line to the patch file
    '''
    if (libmisc.Spritenumchk(Sprite) != 'UNK') & (libmisc.ClassIDcheck(ClassID) != 'UNK'):
        with open(PatchPath, mode='a') as Patch:
            Patch.write(''.join(['{', str(Sprite), '#', str(ClassID), '}', '\n']))
        return 'Done'
