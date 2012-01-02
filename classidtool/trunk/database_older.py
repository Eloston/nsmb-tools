# ClassID Tool
# Database module

def lookup(DatabasePath, ClassID):
    '''
    Looks up the decimal representation of the ClassID in the Name Database
    '''
    Database1 = open(DatabasePath, mode='r')
    Database = Database1.read()
    Database1.close()    
    BracketState = None
    PoundState = None
    ClassIDRead = ''
    DescriptionRead = ''
    ClassIDMatch = None
    for Char in Database:
        if Char == '{':
            BracketState = 'OPEN'
        elif Char == '#':
            PoundState = 'SEEN'
        elif Char == '}':
            BracketState = 'CLOSED'
            if ClassIDMatch == True:
                return DescriptionRead
            if ClassIDMatch == None:
                BracketState = None
                PoundState = None
                ClassIDRead = ''
                DescriptionRead = ''
        else:
            if BracketState == 'OPEN':
                if PoundState != 'SEEN':
                    ClassIDRead = ''.join([ClassIDRead, Char])
                elif PoundState == 'SEEN':
                    if ClassIDRead == str(ClassID):
                        ClassIDMatch = True
            if ClassIDMatch == True:
                DescriptionRead = ''.join([DescriptionRead, Char])
