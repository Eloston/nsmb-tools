# ClassID Tool
# Misc stuff

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
    if 0 <= ClassID <= 65536:
        return ClassID
    else:
        return 'UNK'
