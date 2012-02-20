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
