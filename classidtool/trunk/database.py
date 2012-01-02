# ClassID Tool
# Name Database parsing module

import libmisc
import re

def readdb(NameDB):
    regexp = re.compile(r"\{(?P<ClassID>[0-9]+)\#(?P<Name>.+)\}")
    db = dict()
    with open(NameDB, mode='r') as Database:
        for line in Database:
            m = regexp.match(line)
            db[int(m.group('ClassID'))] = m.group('Name')

    return db

def lookup(db, classid):
    try:
        return db[classid]
    except KeyError:
        return "INVCLASSID"
