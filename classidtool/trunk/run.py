# ClassID Tool
# Friendly interface chooser

import interfacerom
import interfaceoverlay

def interfacechooser():
    print("ClassID Tool")
    print("By nsmbhacking")
    print("---------------")
    while True:
        print("Choose your interface")
        print("A) Open NSMB ROM")
        print("B) Open extracted Overlay0")
        print("C) Close ClassID Tool")
        interfacechooser_choice = input("Choose your option: ")
        print("---------------")
        if interfacechooser_choice.upper() == "A":
            print("*-#-=CAUTION=-#-*")
            print("The Overlay0 in the ROM MUST be decompressed before you access the Overlay0 in the ROM.")
            print("NSMBe is capable of decompressing the Overlay0.")
            print("Without decompressing the Overlay0, this tool may cause severe damage to the ROM, resulting in corruption.")
            print("Do you want to continue?")
            nsmbrom_warning_input = input("Type 'Yes' to continue, or hit [Enter] to cancel: ")
            print("---------------")
            if nsmb_rom_warning_input == "Yes":            
                interfacerom.interface()
            else:
                print("Returning to main menu")
                print("---------------")
        elif interfacechooser_choice.upper() == "B":
            interfaceoverlay.interface()
        elif interfacechooser_choice.upper() == "C":
            quit()
        else:
            print("Invalid option")
            input("Press [Enter] to continue")
            print("---------------")
interfacechooser()
