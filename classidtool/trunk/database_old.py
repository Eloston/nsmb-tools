# ClassID Tool
# Name Database parsing module

import libmisc
import re

def lookup(OVPath, ClassID):
    if libmisc.ClassIDcheck(ClassID) != 'UNK':
        Database = open(OVPath, mode='r')
        regexp = re.compile(r"\{(?P<ClassID>[0-9]+)\#(?P<Name>.+)\}")
        for line in Database:
            asdf = regexp.match(line)
            if asdf.group('ClassID') == str(ClassID):
                Database.close()
                return asdf.group('Name')
    else:
        return 'INVCLASSID'
