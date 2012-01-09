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
