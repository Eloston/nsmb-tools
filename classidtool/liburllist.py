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
# URL List (URL_List.txt) Parser

import re

def importlist(URLList):
    '''
    Import URL List and return a dictionary
    '''
    db = dict()
    regexp = re.compile(r"\{(?P<URLName>.+)\#(?P<URL>.+)\}")
    with open(URLList, mode='r') as LIST:
        for line in LIST:
            m = regexp.match(line)
            if not m == None:
                db[m.group('URLName')] = m.group('URL')

    return db

def lookup(db, value):
    '''
    Lookup URL in URL List dictionary
    '''
    try:
        return db[value]
    except KeyError:
        return "NOTURL"
