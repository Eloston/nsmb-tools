# ClassID Tool
# Misc stuff

import sys
import os.path

def Spritenumchk(Sprite):
    '''    
    Check to make sure the Sprite number is valid
    '''    
    if 1 <= Sprite <= 325:
        return Sprite
    else:
        return 'UNK'

def ClassIDcheck(ClassID):
    '''
    Check to make sure the ClassID value is valid
    '''
    if 0 <= ClassID <= 65535:
        return ClassID
    else:
        return 'UNK'

def programfile_path(FILENAME):
    '''
    Return absolute path to a ClassID Tool program file
    '''
    basepath = os.path.dirname(sys.argv[0])
    if sys.platform.startswith('win32'):
        final_path = ''.join([basepath, '\\', FILENAME])
    else:
        # Assume UNIX-Like OS
        final_path = ''.join([basepath, '/', FILENAME])
    return final_path

def check_file(PATH):
    '''
    Checks if the path refers to a file
    '''
    if os.path.isfile(PATH):
        return PATH
    else:
        return "NOT_FILE"
