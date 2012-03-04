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
# Friendly interface to interface with the ROM

import librom
import database
import libmisc
import libpatch
import ovproc

def specifyrom():
    while True:
        ROM_path = input("Input the absolute or relative path to the ROM: ")
        print("---------------")
        if libmisc.check_file(ROM_path) == "NOT_FILE":
            print("Not a valid file. Try again")
            print("---------------")
        else:
            return ROM_path

def interface():
    # Import and store Name Database
    namedb = database.readdb(libmisc.programfile_path('NameDatabase'))
    # Import and store Patch Original
    patchoriginal = database.read_patch(libmisc.programfile_path('PatchOriginal'))
    # Start interface
    print('ClassID Tool ROM interface')
    print("---------------")
    ROM_path = specifyrom()
    rom_region = librom.detect_region(ROM_path)
    if rom_region == 'UNK':
        print("The ROM region could not be automatically detected. Specify it manually")    
        print("Put USA for United States version")
        print("Put EUR for the European version")
        print("Put JAP for the Japanese version")
        print("And put KOR for the Korean version")
        rom_region = input("Put your version here: ")
        print("---------------")
    else:
        print("Is the ROM region", rom_region, "correct?")
        romregionconfirm = input("Press [Enter] to accept, or type N to specify your own: ")
        if romregionconfirm.upper() == "N":
            print("Input the ROM Region")
            print("Put USA for United States version")
            print("Put EUR for the European version")
            print("Put JAP for the Japanese version")
            print("And put KOR for the Korean version")
            rom_region = input("Put your version here: ")
            print("---------------")
    OVERLAY_OFFSET = librom.get_overlay_offset(ROM_path, ovproc.ovoffset(rom_region))
    while True:
        print("Choose your options:")
        print("A) Read ClassID")
        print("B) Write ClassID")
        print("C) Import Patch")
        print("D) Export Patch")
        print("E) Change ROM region")
        print("F) Change ROM path")
        print("G) Reload Overlay0, Sprite 1 Offset")
        print("H) Quit ROM interface and return to interface chooser")
        menu_option = input("Choose your option: ")
        print("---------------")
        if menu_option.upper() == "A":
            while True:            
                sprite_input = input("Specify the Sprite you want to look up the Class ID of: ")
                print("---------------")
                try:
                    sprite_input = int(sprite_input)
                    break
                except ValueError:
                    print("Not a valid sprite value. Try again")
                    input("Press [Enter] to continue")
                    print("---------------")
            classid_read_result = librom.ClassIDread(ROM_path, sprite_input, OVERLAY_OFFSET)
            if classid_read_result == 'INVSPRITE':
                print("Invalid Sprite Number: Out of range")
                print("---------------")
            else:
                print("The Class ID for Sprite", sprite_input, "is", classid_read_result, 'which is named', database.lookup(namedb, classid_read_result))
                input("Press [Enter] to continue")
                print("---------------")
        elif menu_option.upper() == "B":
            while True:            
                sprite_input = input("Specify the Sprite you want to change the Class ID of: ")
                print("---------------")
                try:
                    sprite_input = int(sprite_input)
                    break
                except ValueError:
                    print("Not a valid sprite value. Try again")
                    input("Press [Enter] to continue")
                    print("---------------")
            while True:            
                classid_input = input("Specify the Class ID you want to change the sprite to: ")
                print("---------------")
                try:
                    classid_input = int(classid_input)
                    break
                except ValueError:
                    print("Not a valid Class ID. Try again")
                    input("Press [Enter] to continue")
                    print("---------------")
            classid_write_result = librom.ClassIDwrite(ROM_path, sprite_input, classid_input, OVERLAY_OFFSET)
            if classid_write_result == "INVCLASSIDSPRITE":
                print("Your Sprite value and/or Class ID were not valid: Out of Range")
                input("Press [Enter] to continue")
                print("---------------")
            else:
                print("You wrote", classid_input, "which is", database.lookup(namedb, classid_input), "to Sprite", sprite_input)
                input("Press [Enter] to continue")
                print("---------------")
        elif menu_option.upper() == "C":
            patch_input = input("Specify the absolute or relative path to the patch: ")
            print("This may take a few seconds depending on the size of the patch")
            print("---------------")
            patch_input = database.read_patch(patch_input)
            libpatch.import_patch_rom(patch_input, ROM_path, OVERLAY_OFFSET)
            print("Done")
            print("---------------")
        elif menu_option.upper() == "D":
            patch_input = input("Specify where you want the patch to be written to: ")
            print("This may take a few seconds depending on the number of differences")
            print("---------------")
            libpatch.create_patch_rom(patch_input, patchoriginal, ROM_path, OVERLAY_OFFSET)
            print("Done")
            print("---------------")
        elif menu_option.upper() == "E":
            rom_region = librom.detect_region(ROM_path)
            if rom_region == 'UNK':
                print("The ROM region could not be automatically detected. Specify it manually")    
                print("Put USA for United States version")
                print("Put EUR for the European version")
                print("Put JAP for the Japanese version")
                print("And put KOR for the Korean version")
                rom_region = input("Put your version here: ")
                print("---------------")
            else:
                print("Is the ROM region", rom_region, "correct?")
                romregionconfirm = input("Press [Enter] to accept, or type N to specify your own: ")
                print("---------------")
                if romregionconfirm.upper() == "N":
                    print("Input the ROM Region")
                    print("Put USA for United States version")
                    print("Put EUR for the European version")
                    print("Put JAP for the Japanese version")
                    print("And put KOR for the Korean version")
                    rom_region = input("Put your version here: ")
                    print("---------------")
        elif menu_option.upper() == "F":
            ROM_path = specifyrom()
        elif menu_option.upper() == "G":
            OVERLAY_OFFSET = librom.get_overlay_offset(ROM_path, ovproc.ovoffset(rom_region))
            print("Done. The offset is now", OVERLAY_OFFSET)
            input("Press [Enter] to continue")
            print("---------------")
        elif menu_option.upper() == "H":
            return None
        else:
            print("Invalid option")
            input("Press [Enter] to continue")
            print("---------------")
