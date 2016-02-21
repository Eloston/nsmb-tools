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
# GUI interface

from PyQt4 import QtCore, QtGui

import librom
import ovproc
import libpatch
import libmisc
import libupdate
import database
import os.path

class interface(QtGui.QMainWindow):
    def __init__(self):
        super(interface, self).__init__()

        global ToolName

        self.fileInfoTab = FileInfoTab()
        self.classIDEditingTab = ClassIDEditingTab()

        self.tabs = QtGui.QTabWidget()
        self.tabs.addTab(self.fileInfoTab, "File Info")
        self.tabs.addTab(self.classIDEditingTab, "ClassID Editing")
        self.setCentralWidget(self.tabs)

        statusbarwelcome = ''.join(["Welcome to ", ToolName])
        self.statusBar().showMessage(statusbarwelcome)

        # Define submenus and linking functions
        self.openAct = QtGui.QAction("&Open", self, statusTip="Open a NDS ROM or Overlay0", triggered=self.openfile)
        self.closeAct = QtGui.QAction("&Close", self, statusTip="Close the opened NDS ROM or Overlay0", triggered=self.closefile)        
        self.exitAct = QtGui.QAction("&Exit", self, statusTip=''.join(["Exit ", ToolName]), triggered=self.close)

        self.importPatchAct = QtGui.QAction("&Import Patch...", self, statusTip="Import a patch", triggered=self.importPatch)
        self.exportPatchAct = QtGui.QAction("&Export Patch...", self, statusTip="Export a patch", triggered=self.exportPatch)

        self.lookupnameAct = QtGui.QAction("&Lookup ClassID Name", self, statusTip="Lookup the name of a ClassID", triggered=self.lookupname)
        self.resetClassIDAct = QtGui.QAction("&Reset ClassID values", self, statusTip="Restore the original ClassID values", triggered=self.resetClassID)

        self.updateNameDBAct = QtGui.QAction("&NameDatabase", self, statusTip="Update the NameDatabase file", triggered=self.updateNameDB)

        self.setascending_extraAct = QtGui.QAction("&Ascending values 1:1 mapping", self, statusTip="Sprite # = ClassID!", triggered=self.setascending_extra)

        self.helpAct = QtGui.QAction(''.join(["&About ", ToolName]), self, statusTip=''.join(["View information about ", ToolName]), triggered=self.abouttool)

        # Define Menus
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.closeAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.patchMenu = self.menuBar().addMenu("&Patching")
        self.patchMenu.addAction(self.importPatchAct)
        self.patchMenu.addAction(self.exportPatchAct)

        self.toolMenu = self.menuBar().addMenu("&Tools")
        self.toolMenu.addAction(self.lookupnameAct)
        self.toolMenu.addAction(self.resetClassIDAct)
        self.toolMenu.addSeparator()

        self.updateMenu = self.toolMenu.addMenu("&Update")
        self.updateMenu.addAction(self.updateNameDBAct)

        self.extrasMenu = self.toolMenu.addMenu("&Extras")
        self.extrasMenu.addAction(self.setascending_extraAct)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.helpAct)

        self.setWindowTitle(ToolName)

        self.closefile()

    # Define menu action
    def openfile(self):
        global filePath
        global ReadOnly
        ReadOnly = False
        filePath = QtGui.QFileDialog.getOpenFileName(self, "Open Overlay0 or NDS ROM", '', "NDS ROM (*.nds);;All/Overlay0 Files (*)")
        if filePath == '':
            return None
        try:
            # Best way to check if file exists and is readable at the same time
            os.path.getsize(filePath)
        except:
            QtGui.QMessageBox.critical(self, "Error while opening", "The file you have specified could not be read.\nThis may be caused because you don't have reading rights, or another reason.", "OK")
            return None
        try:
            # Is file writeable?
            readonlytest = open(filePath, mode='r+b')
            readonlytest.close()
        except:
            QtGui.QMessageBox.information(self, "File detected as read-only", "The file you have selected has been detected and will be opened in read-only mode.")
            ReadOnly = True
        if File_Interface.DetectFileType() == "Overlay0":
            filetypeanswer = 1
        elif File_Interface.DetectFileType() == "NDS ROM":
            filetypeanswer = 2
        else:
            filetypeanswer = QtGui.QMessageBox.question(self, "NDS ROM or Overlay0?", "Unable to detect the file type.\nIf it is an Overlay0, then select the Overlay0 button.\nIf it is a NDS ROM, select the NDS ROM button.", "Cancel", "Overlay0", "NDS ROM")
        global fileType
        if filetypeanswer == 1:
            fileType = "Overlay0"
            self.detectregion()
            self.openAct.setEnabled(False)
            self.closeAct.setEnabled(True)
            if not ReadOnly:
                self.importPatchAct.setEnabled(True)
                self.exportPatchAct.setEnabled(True)
                self.resetClassIDAct.setEnabled(True)
                self.extrasMenu.setEnabled(True)
            FileInfoTab.load_info(self.fileInfoTab)
            ClassIDEditingTab.load_file(self.classIDEditingTab)
        elif filetypeanswer == 2:
            fileType = "NDS ROM"
            File_Interface.CheckOverlay0()
            self.detectregion()
            self.openAct.setEnabled(False)
            self.closeAct.setEnabled(True)
            if not ReadOnly:                
                self.importPatchAct.setEnabled(True)
                self.exportPatchAct.setEnabled(True)
                self.resetClassIDAct.setEnabled(True)
                self.extrasMenu.setEnabled(True)
            global ROMOvOffset
            ROMOvOffset = librom.get_overlay_offset(filePath, ovproc.ovoffset(fileRegion))
            ClassIDEditingTab.load_file(self.classIDEditingTab)
            FileInfoTab.load_info(self.fileInfoTab)

    def closefile(self):
        self.openAct.setEnabled(True)
        self.closeAct.setEnabled(False)
        self.importPatchAct.setEnabled(False)
        self.exportPatchAct.setEnabled(False)
        self.resetClassIDAct.setEnabled(False)
        self.extrasMenu.setEnabled(False)
        global filePath
        global fileType
        global fileRegion
        global ROMOvOffset
        filePath = None
        fileType = None
        fileRegion = None
        ROMOvOffset = None
        ClassIDEditingTab.close_file(self.classIDEditingTab)
        FileInfoTab.clear_info(self.fileInfoTab)

    def importPatch(self):
        patchPath = QtGui.QFileDialog.getOpenFileName(self, "Open a Patch file", '', "Patch Files (*)")
        if not patchPath == '':
            File_Interface.ImportPatch(database.read_patch(patchPath))
            ClassIDEditingTab.close_file(self.classIDEditingTab)
            ClassIDEditingTab.load_file(self.classIDEditingTab)
            QtGui.QMessageBox.information(self, "Patching Operation result", ' '.join(["The patch", patchPath, "has been imported and patched sucessfully"]))

    def resetClassID(self):
        ConfirmReset = QtGui.QMessageBox.warning(self, "Confirm ClassID values reset", "If you click Yes, you will loose all ClassID value changes.\nAre you sure you want to continue?", "No", "Yes")
        if ConfirmReset == 1:
            global PatchOrig
            File_Interface.ImportPatch(PatchOrig)
            ClassIDEditingTab.close_file(self.classIDEditingTab)
            ClassIDEditingTab.load_file(self.classIDEditingTab)
            QtGui.QMessageBox.information(self, "Reset ClassIDs to Default values result", "The ClassIDs have been restored to the original values sucessfully.")

    def exportPatch(self):
        NewPatch = QtGui.QFileDialog.getSaveFileName(self, "Choose a location for the new Patch", '', "Patch Files (*)")
        if not NewPatch == '':
            File_Interface.ExportPatch(NewPatch)
            QtGui.QMessageBox.information(self, "Patch Exporting result", ' '.join(["The patch", NewPatch, "has been created sucessfully."]))

    def lookupname(self):
        self.LookupNameDialog = NameDBTable()
        NameDBTable.LookupClassID(self.LookupNameDialog)

    def abouttool(self):
        global ToolName
        QtGui.QMessageBox.about(self, ''.join(["About ", ToolName]) ,''.join([ToolName, "\n    By Eloston (aka ELMario)\n", ToolName, " is a tool to modify, read, and lookup names for Class IDs from a NSMB ROM or an extracted Overlay0 from a NSMB ROM."]))

    # Other misc. functions
    def chooseregion(self):
        global fileRegion
        friendly_region_names = ("United States", "European", "Japanese", "Korean")
        ok = False
        while ok == False:
            choice, ok = QtGui.QInputDialog.getItem(self, "Choose a Region", "Choose the region of the Overlay0 or ROM manually below:", friendly_region_names, 0, False)
        fileRegion = self.convert_region(choice)

    def chooseregion2(self):
        global fileRegion
        friendly_region_names = ("United States", "European", "Japanese", "Korean")
        choice, ok = QtGui.QInputDialog.getItem(self, "Choose a Region", "Choose the region of the Overlay0 or ROM manually below:", friendly_region_names, 0, False)
        if ok:
            fileRegion = self.convert_region(choice)

    def detectregion(self):
        global fileRegion
        File_Interface.file_region()
        if fileRegion == 'UNK':
            self.chooseregion()

    def updateNameDB(self):
        try:
            testreadonly = open(libmisc.programfile_path("NameDatabase"), mode='r+b')
            testreadonly.close()
        except:
            QtGui.QMessageBox.critical(self, "Error while updating", "The NameDatabase cannot be edited.\nMake sure you can edit NameDatabase before updating.", "OK")
            return None
        result_code, result_message = libupdate.update_namedatabase(libmisc.programfile_path("NameDatabase"), libmisc.programfile_path("URLList"))
        if result_code == "urllist-parse-failure":
            QtGui.QMessageBox.critical(self, "Error while updating", "Failed to read the URLList file.\nCheck to see if the file is readable and is not corrupt.\nError message: " + result_message, "OK")
        elif result_code == "download-failure":
            QtGui.QMessageBox.critical(self, "Error while updating", "Failed to download the new NameDatabase file.\nCheck to see if the URL in the URLList file is downloadable.\nError message: " + result_message, "OK")
        elif result_code == "write-failure":
            QtGui.QMessageBox.critical(self, "Error while updating", "The new NameDatabase cannot be written.\nMake sure you can edit the NameDatabase file before trying again.\nError message: " + result_message, "OK")
        elif result_code == "success":
            global NameDB
            global fileType
            NameDB = database.readdb(libmisc.programfile_path("NameDatabase"))
            if not fileType == None:
                self.classIDEditingTab.close_file()
                self.classIDEditingTab.load_file()
            QtGui.QMessageBox.information(self, "Updating results", "The NameDB has updated sucessfully", "OK")

    def setascending_extra(self):
        '''
        Set all sprite values and ClassIDs to a 1:1 mapping (sprite 1 -> classid 1, sprite 2 -> classid 2, etc)
        Just for fun and convenience
        Kinda hackish
        '''
        NewPatch = dict()
        iterate = 1
        while iterate <= 325:
            NewPatch[iterate] = iterate
            iterate = iterate + 1
        File_Interface.ImportPatch(NewPatch)
        ClassIDEditingTab.close_file(self.classIDEditingTab)
        ClassIDEditingTab.load_file(self.classIDEditingTab)
        QtGui.QMessageBox.information(self, "Operation finished", "All Sprites have been set to a ClassID by a 1:1 mapping.")
        

    @staticmethod
    def convert_region(INPUT):
        if INPUT == "USA":
            return "United States"
        elif INPUT == "EUR":
            return "European"
        elif INPUT == "JAP":
            return "Japanese"
        elif INPUT == "KOR":
            return "Korean"
        elif INPUT == "United States":
            return "USA"
        elif INPUT == "European":
            return "EUR"
        elif INPUT == "Japanese":
            return "JAP"
        elif INPUT == "Korean":
            return "KOR"

class NameDBTable(QtGui.QDialog):
    def __init__(self, parent=None):
        super(NameDBTable, self).__init__(parent)

        self.classnametable = QtGui.QTableWidget(0, 2)

        self.classnametable.setHorizontalHeaderLabels(("ClassID", "ClassID Name"))
        self.classnametable.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self.classnametable.verticalHeader().hide()
        self.classnametable.setShowGrid(True)
        self.classnametable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        TopLabel = QtGui.QLabel("Below is a list of known ClassIDs and their names")

        self.Layout = QtGui.QVBoxLayout()
        self.Layout.addWidget(TopLabel)

    def LookupClassID(self):
        global ToolName
        self.setWindowTitle(''.join([ToolName, " - Lookup ClassID Names"]))

        self.closebutton = QtGui.QPushButton("Close")
        self.closebutton.clicked.connect(self.close)

        buttonFiller = QtGui.QWidget()
        buttonFiller.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(buttonFiller)
        buttonLayout.addWidget(self.closebutton)

        self.Layout.addWidget(self.classnametable)
        self.Layout.addLayout(buttonLayout)
        self.setLayout(self.Layout)

        self.UpdateTable()
        self.show()

    def ChangeClassID(self, currentSprite):
        global ToolName
        self.setWindowTitle(''.join([ToolName, " - Change ClassID Value"]))

        self.currentSprite = currentSprite

        self.classnametable.cellActivated.connect(self.ChangeClassID_setlinevalue)

        self.SelectedValue = None

        self.okbutton = QtGui.QPushButton("OK")
        self.okbutton.clicked.connect(self.ChangeClassID_finished)

        self.closebutton = QtGui.QPushButton("Cancel")
        self.closebutton.clicked.connect(self.close)

        self.SelectedClassIDBox = QtGui.QSpinBox()
        self.SelectedClassIDBox.setRange(0, 65535)
        self.SelectedClassIDBox.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)

        Name_SelectedClassIDBox = QtGui.QLabel(''.join(["Choose a ClassID for Sprite ", str(self.currentSprite), ":"]))

        buttonFiller = QtGui.QWidget()
        buttonFiller.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)

        valueboxLayout = QtGui.QHBoxLayout()
        valueboxLayout.addWidget(Name_SelectedClassIDBox)
        valueboxLayout.addWidget(self.SelectedClassIDBox)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(buttonFiller)
        buttonLayout.addWidget(self.okbutton)
        buttonLayout.addWidget(self.closebutton)

        InformationLabel = QtGui.QLabel("Double-Click an entry above to automatically set the spinbox to that ClassID")

        self.Layout.addWidget(self.classnametable)
        self.Layout.addWidget(InformationLabel)
        self.Layout.addLayout(valueboxLayout)
        self.Layout.addLayout(buttonLayout)
        self.setLayout(self.Layout)

        self.UpdateTable()
        self.show()

    def ChangeClassID_finished(self):
        self.SelectedValue = self.SelectedClassIDBox.value()
        Interface.classIDEditingTab.editclassid_checkchange(self.SelectedValue, self.currentSprite)
        self.close()

    def ChangeClassID_setlinevalue(self):
        currentRow = self.classnametable.currentRow()
        currentClassID = self.classnametable.item(currentRow, 0).text()
        self.SelectedClassIDBox.setValue(int(currentClassID))

    def UpdateTable(self):
        self.classnametable.clearContents()
        self.classnametable.setRowCount(0)
        global NameDB
        iterate = 0
        for IDVALUE in list(NameDB.keys()):
            ClassIDTableValue = QtGui.QTableWidgetItem(str(IDVALUE))
            ClassIDTableValue.setFlags(ClassIDTableValue.flags() ^ QtCore.Qt.ItemIsEditable)
            ClassIDTableName = QtGui.QTableWidgetItem(NameDB[IDVALUE])
            ClassIDTableName.setFlags(ClassIDTableName.flags() ^ QtCore.Qt.ItemIsEditable)

            self.classnametable.insertRow(iterate)
            self.classnametable.setItem(iterate, 0, ClassIDTableValue)
            self.classnametable.setItem(iterate, 1, ClassIDTableName)
            iterate = iterate + 1

class FileInfoTab(QtGui.QWidget):
    def __init__(self, parent=None):
        super(FileInfoTab, self).__init__(parent)

        Name_Label_File_Type = QtGui.QLabel("Type: ")
        Name_Label_File_Type.setToolTip("The type of file currently open")
        self.Label_File_Type = QtGui.QLabel("N/A")
        
        Name_Label_ROM_Region = QtGui.QLabel("Region: ")
        Name_Label_ROM_Region.setToolTip("This is the region of the opened file. Different regions are opened differently")
        self.Label_ROM_Region = QtGui.QLabel("N/A")
        
        Name_Text_File_Path = QtGui.QLabel("File Path: ")
        Name_Text_File_Path.setToolTip("The absolute path to the opened file")
        self.Text_File_Path = QtGui.QLineEdit()
        self.Text_File_Path.setReadOnly(True)

        Name_Text_ROM_OverlayOffset = QtGui.QLabel("ROM Overlay0 Offset: ")
        Name_Text_ROM_OverlayOffset.setToolTip("The decimal representation of the offset to Sprite 1 in the ROM.\nThis will only show a number when a ROM is open.")
        self.Text_ROM_OverlayOffset = QtGui.QLineEdit()
        self.Text_ROM_OverlayOffset.setReadOnly(True)

        Name_ReadOnly_State = QtGui.QLabel("File opened in read-only mode: ")
        Name_ReadOnly_State.setToolTip("Tells whether the file is opened in read-only mode")
        self.ReadOnly_State = QtGui.QLabel("N/A")

        bottomFiller = QtGui.QWidget()
        bottomFiller.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        self.clear_info()

        layout = QtGui.QGridLayout()
        layout.addWidget(Name_Label_File_Type, 0, 0)
        layout.addWidget(self.Label_File_Type, 0, 1)
        layout.addWidget(Name_Label_ROM_Region, 1, 0)
        layout.addWidget(self.Label_ROM_Region, 1, 1)
        layout.addWidget(Name_Text_File_Path, 2, 0)
        layout.addWidget(self.Text_File_Path, 2, 1)
        layout.addWidget(Name_Text_ROM_OverlayOffset, 3, 0)
        layout.addWidget(self.Text_ROM_OverlayOffset, 3, 1)
        layout.addWidget(Name_ReadOnly_State, 4, 0)
        layout.addWidget(self.ReadOnly_State, 4, 1)

        layoutfiller = QtGui.QVBoxLayout()
        layoutfiller.addLayout(layout)
        layoutfiller.addWidget(bottomFiller)
        self.setLayout(layoutfiller)

    def clear_info(self):
        self.Text_File_Path.setText("N/A")
        self.Text_ROM_OverlayOffset.setText("N/A")
        self.Label_ROM_Region.setText("N/A")
        self.Text_File_Path.setText("N/A")
        self.Label_File_Type.setText("N/A")
        self.ReadOnly_State.setText("N/A")

    def load_info(self):
        global fileType
        global filePath
        global fileRegion
        global Interface
        global ReadOnly
        self.Label_File_Type.setText(fileType)
        self.Label_ROM_Region.setText(interface.convert_region(fileRegion))
        self.Text_File_Path.setText(filePath)
        if ReadOnly:
            self.ReadOnly_State.setText("Yes")
        else:
            self.ReadOnly_State.setText("No")
        if fileType == "NDS ROM":
            global ROMOvOffset
            self.Text_ROM_OverlayOffset.setText(str(ROMOvOffset))

class ClassIDEditingTab(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ClassIDEditingTab, self).__init__(parent)

        self.classidTable = QtGui.QTableWidget(0, 2)

        self.classidTable.setHorizontalHeaderLabels(("ClassID Name", "ClassID"))
        self.classidTable.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.classidTable.setShowGrid(True)
        self.classidTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.classidTable.cellActivated.connect(self.editclassid)

        InstructionLabel = QtGui.QLabel("Double-click an entry to edit the ClassID of that Sprite")
        
        self.Layout = QtGui.QVBoxLayout()
        self.Layout.addWidget(InstructionLabel)
        self.Layout.addWidget(self.classidTable)
        self.setLayout(self.Layout)

    def close_file(self):
        self.classidTable.clearContents()
        self.classidTable.setRowCount(0)

    def load_file(self):
        iterate = 1
        while iterate <= 325:
            ClassIDTableName = File_Interface.NameLookup(File_Interface.ClassIDRead(iterate))
            if ClassIDTableName.upper() == 'INVVALUE':
                ClassIDTableName = QtGui.QTableWidgetItem("(Untitled)")
            else:
                ClassIDTableName = QtGui.QTableWidgetItem(ClassIDTableName)
            ClassIDTableName.setFlags(ClassIDTableName.flags() ^ QtCore.Qt.ItemIsEditable)
            ClassIDTableValue = QtGui.QTableWidgetItem(str(File_Interface.ClassIDRead(iterate)))
            ClassIDTableValue.setFlags(ClassIDTableValue.flags() ^ QtCore.Qt.ItemIsEditable)

            self.classidTable.insertRow(iterate-1)
            self.classidTable.setItem(iterate-1, 0, ClassIDTableName)
            self.classidTable.setItem(iterate-1, 1, ClassIDTableValue)
            iterate = iterate + 1

    def editclassid(self):
        global ReadOnly
        if not ReadOnly:
            currentSprite = self.classidTable.currentRow() + 1
            self.EditClassIDDialog = NameDBTable()
            NameDBTable.ChangeClassID(self.EditClassIDDialog, currentSprite)

        else:
            QtGui.QMessageBox.critical(self, "Error while editing", "This file is in read-only mode.", "OK")

    def editclassid_checkchange(self, choice, currentSprite):
        if not choice == None:
            File_Interface.ClassIDWrite(currentSprite, choice)
            ClassIDTableName = File_Interface.NameLookup(choice)
            if ClassIDTableName.upper() == 'INVVALUE':
                ClassIDTableName = QtGui.QTableWidgetItem("(Untitled)")
            else:
                ClassIDTableName = QtGui.QTableWidgetItem(ClassIDTableName)
            ClassIDTableName.setFlags(ClassIDTableName.flags() ^ QtCore.Qt.ItemIsEditable)
            ClassIDTableValue = QtGui.QTableWidgetItem(str(File_Interface.ClassIDRead(currentSprite)))
            ClassIDTableValue.setFlags(ClassIDTableValue.flags() ^ QtCore.Qt.ItemIsEditable)

            self.classidTable.setItem(currentSprite-1, 0, ClassIDTableName)
            self.classidTable.setItem(currentSprite-1, 1, ClassIDTableValue)

class File_Interface():
    @staticmethod
    def file_region():
        global filePath
        global fileType
        global fileRegion
        if fileType == 'Overlay0':
            fileRegion = ovproc.region_detect(filePath)
        elif fileType == 'NDS ROM':
            fileRegion = librom.detect_region(filePath)

    @staticmethod
    def ClassIDRead(ParamA):
        global filePath
        global fileType
        global fileRegion
        global ROMOvOffset
        if fileType == 'Overlay0':
            return ovproc.ClassIDread(filePath, ParamA, fileRegion)
        elif fileType == 'NDS ROM':
            return librom.ClassIDread(filePath, ParamA, ROMOvOffset)

    @staticmethod
    def ClassIDWrite(ParamA, ParamB):
        global filePath
        global fileType
        global fileRegion
        global ROMOvOffset
        if fileType == 'Overlay0':
            ovproc.ClassIDwrite(filePath, ParamA, fileRegion, ParamB)
        elif fileType == 'NDS ROM':
            librom.ClassIDwrite(filePath, ParamA, ParamB, ROMOvOffset)

    @staticmethod
    def ImportPatch(ParamA):
        global filePath
        global fileType
        global fileRegion
        global ROMOvOffset
        if fileType == 'Overlay0':
            libpatch.import_patch(ParamA, filePath, fileRegion)
        elif fileType == 'NDS ROM':
            libpatch.import_patch_rom(ParamA, filePath, ROMOvOffset)

    @staticmethod
    def ExportPatch(ParamA):
        global filePath
        global fileType
        global fileRegion
        global ROMOvOffset
        global PatchOrig
        if fileType == 'Overlay0':
            libpatch.create_patch(ParamA, PatchOrig, filePath, fileRegion)
        elif fileType == 'NDS ROM':
            libpatch.create_patch_rom(ParamA, PatchOrig, filePath, ROMOvOffset)

    @staticmethod
    def NameLookup(ParamA):
        global NameDB
        return database.lookup(NameDB, ParamA)

    @staticmethod
    def DetectFileType():
        global filePath
        if ovproc.check_header(filePath):
            return "Overlay0"
        elif librom.check_header(filePath):
            return "NDS ROM"
        else:
            return False

    @staticmethod
    def CheckOverlay0():
        global filePath
        if not librom.CheckOverlay0Decompressed(filePath):
            librom.DecompressOverlay0(filePath)

class Missingfilesdialog(QtGui.QWidget):
    def __init__(self):
        super(Missingfilesdialog, self).__init__()

        global Missingfiles
        global ToolName

        self.ErrorMessage = QtGui.QLabel(''.join([ToolName, " is unable to load without the following file(s):"]))
        self.MissingList = QtGui.QTextEdit()
        self.MissingList.setPlainText(Missingfiles)
        self.MissingList.setReadOnly(True)
        self.ErrorMessageBottom = QtGui.QLabel("Close this and make the file(s) avaliable to load.")
        self.closebutton = QtGui.QPushButton("Close")
        self.closebutton.clicked.connect(self.close)

        buttonFiller = QtGui.QWidget()
        buttonFiller.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(buttonFiller)
        buttonLayout.addWidget(self.closebutton)

        self.Layout = QtGui.QVBoxLayout()
        self.Layout.addWidget(self.ErrorMessage)
        self.Layout.addWidget(self.MissingList)
        self.Layout.addWidget(self.ErrorMessageBottom)
        self.Layout.addLayout(buttonLayout)

        self.setLayout(self.Layout)

        self.setWindowTitle(''.join([ToolName, " - Error"]))

class GeneralExceptiondialog(QtGui.QDialog):
    def __init__(self, *args):
        super(GeneralExceptiondialog, self).__init__()

        import traceback
        ExceptionDetails = ''.join(traceback.format_exception(*args))
        global ToolName

        self.ErrorMessage = QtGui.QLabel(''.join([ToolName, " has encountered an error. The details are below:"]))
        self.MissingList = QtGui.QTextEdit()
        self.MissingList.setPlainText(ExceptionDetails)
        self.MissingList.setReadOnly(True)
        self.ErrorMessageBottom = QtGui.QLabel("You may be seeing this if your Overlay 0 or ROM file is corrupt.<br />If this is not the case, please submit these details to the GitHub Issue Tracker: <a href=\"https://github.com/Eloston/nsmb-tools/issues\">https://github.com/Eloston/nsmb-tools/issues</a>")
        self.closebutton = QtGui.QPushButton("Close")
        self.closebutton.clicked.connect(self.close)

        buttonFiller = QtGui.QWidget()
        buttonFiller.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(buttonFiller)
        buttonLayout.addWidget(self.closebutton)

        self.Layout = QtGui.QVBoxLayout()
        self.Layout.addWidget(self.ErrorMessage)
        self.Layout.addWidget(self.MissingList)
        self.Layout.addWidget(self.ErrorMessageBottom)
        self.Layout.addLayout(buttonLayout)

        self.setLayout(self.Layout)

        self.setWindowTitle(''.join([ToolName, " - Error"]))

def exceptionhookstart(*args):
    global ExceptionDialog
    QtGui.qApp.closeAllWindows()
    ExceptionDialog = GeneralExceptiondialog(*args)
    ExceptionDialog.show()

filePath = None
fileType = None
fileRegion = None
ROMOvOffset = None
NameDB = None
PatchOrig = None
ReadOnly = None
ToolName = "ClassID Tool 6.1"

ExceptionDialog = None

if __name__ == '__main__':
    import sys

    sys.excepthook = exceptionhookstart

    app = QtGui.QApplication(sys.argv)

    Missingfiles = ''
    try:
        NameDB = database.readdb(libmisc.programfile_path("NameDatabase"))
    except:
        Missingfiles = Missingfiles + 'NameDatabase\n'
    try:
        PatchOrig = database.read_patch(libmisc.programfile_path("PatchOriginal"))
    except:
        Missingfiles = Missingfiles + 'PatchOriginal\n'
    if not os.path.exists(libmisc.programfile_path("URLList")):
        Missingfiles = Missingfiles + 'URLList\n'
    if len(Missingfiles) == 0:
            Interface = interface()
            Interface.show()
    else:
        missingfilesdialog = Missingfilesdialog()
        missingfilesdialog.show()

    sys.exit(app.exec_())
