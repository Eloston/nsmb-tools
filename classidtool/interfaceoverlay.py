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
# Friendly interface to interface with the extracted Overlay0

import ovproc
import database
import libmisc
import libpatch

def specifyoverlay():
    while True:
        overlay_path = input("Input the absolute or relative path to the extracted Overlay0: ")
        print("---------------")
        if libmisc.check_file(overlay_path) == "NOT_FILE":
            print("Not a valid file. Try again")
            print("---------------")
        else:
            return ROM_path

def checkromregion():
    rom_region = ovproc.region_detect(overlay_path)
    if rom_region == 'UNK':
        print("The Overlay region could not be automatically detected. Specify it manually")    
        print("Put USA for United States version")
        print("Put EUR for the European version")
        print("Put JAP for the Japanese version")
        print("And put KOR for the Korean version")
        rom_region = input("Put your version here: ")
        print("---------------")
    else:
        print("Is the Overlay region", rom_region, "correct?")
        romregionconfirm = input("Press [Enter] to accept, or type N to specify your own: ")
        if romregionconfirm.upper() == "N":
            print("Input the ROM Region of the overlay")
            print("Put USA for United States version")
            print("Put EUR for the European version")
            print("Put JAP for the Japanese version")
            print("And put KOR for the Korean version")
            rom_region = input("Put your version here: ")
            print("---------------")
    return rom_region

def interface():
    # Import and store Name Database
    namedb = database.readdb(libmisc.programfile_path('NameDatabase'))
    # Import and store Patch Original
    patchoriginal = database.read_patch(libmisc.programfile_path('PatchOriginal'))
    # Begin Interface
    print('ClassID Tool external Overlay0 Interface')
    overlay_path = specifyoverlay()
    rom_region = checkromregion()
    while True:
        print("Choose your option:")
        print("A) Read Class ID")
        print("B) Write Class ID")
        print("C) Lookup Class ID")
        print("D) Change Overlay0 Region")
        print("E) Change Overlay0 Path")
        print("F) Restart Class ID Tool")
        print("G) Return to ClassID Tool friendly interface chooser")
        print("H) Import Patch")
        print("I) Export Patch")
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
            classid_read_result = ovproc.ClassIDread(overlay_path, sprite_input, rom_region)
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
            classid_write_result = ovproc.ClassIDwrite(overlay_path, sprite_input, rom_region, classid_input)
            if classid_write_result == "INVCLASSIDSPRITE":
                print("Your Sprite value and/or Class ID were not valid: Out of Range")
                input("Press [Enter] to continue")
                print("---------------")
            else:
                print("You wrote", classid_input, "which is", database.lookup(namedb, classid_input), "to Sprite", sprite_input)
        elif menu_option.upper() == "C":
            while True:            
                classid_input = input("Specify the Class ID you want to look the name of up: ")
                print("---------------")
                try:
                    classid_input = int(classid_input)
                    break
                except ValueError:
                    print("Not a valid Class ID. Try again")
                    input("Press [Enter] to continue")
                    print("---------------")
            lookup_result = database.lookup(namedb, classid_input)
            if lookup_result == "INVCLASSID":
                print("The Class ID you specified is not valid.")
                input("Press [Enter] to continue")
            else:
                print("The name of the Class ID is:", lookup_result)
                input("Press [Enter] to continue")
                print("---------------")
        elif menu_option.upper() == "D":
            rom_region = checkromregion()
        elif menu_option.upper() == "E":
            overlay_path = specifyoverlay()
        elif menu_option.upper() == "F":
            print("Not implemented yet. Do option G and run Class ID Tool again.")
            input("Press [Enter] to continue")
            print("---------------")
        elif menu_option.upper() == "G":
            return None
        elif menu_option.upper() == "H":
            patch_input = input("Specify the absolute or relative path to the patch: ")
            print("This may take a few seconds depending on the size of the patch")
            print("---------------")
            patch_input = database.read_patch(patch_input)
            libpatch.import_patch(patch_input, overlay_path, rom_region)
            print("Done")
            print("---------------")
        elif menu_option.upper() == "I":
            patch_input = input("Specify where you want the patch to be written to: ")
            print("This may take a few seconds depending on the number of differences")
            print("---------------")
            libpatch.create_patch(patch_input, patchoriginal, overlay_path, rom_region)
            print("Done")
            print("---------------")
        else:
            print("Invalid option")
            input("Press [Enter] to continue")
            print("---------------")
