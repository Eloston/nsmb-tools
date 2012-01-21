# ClassID Tool
# Friendly GUI interface

from PyQt4 import QtCore, QtGui

import librom
import ovproc
import libpatch
import libmisc
import database

class interface(QtGui.QMainWindow):
    def __init__(self):
        super(interface, self).__init__()

        self.fileInfoTab = FileInfoTab()
        self.classIDEditingTab = ClassIDEditingTab()

        self.tabs = QtGui.QTabWidget()
        self.tabs.addTab(self.fileInfoTab, "File Info")
        self.tabs.addTab(self.classIDEditingTab, "ClassID Editing")
        self.setCentralWidget(self.tabs)

        # Define submenus and linking functions
        self.openAct = QtGui.QAction("&Open", self, statusTip="Open a NDS ROM or Overlay0", triggered=self.openfile)
        self.closeAct = QtGui.QAction("&Close", self, statusTip="Close the opened NDS ROM or Overlay0", triggered=self.closefile)        
        self.exitAct = QtGui.QAction("&Exit", self, statusTip="Exit ClassID Tool", triggered=self.close)

        self.importPatchAct = QtGui.QAction("&Import Patch...", self, statusTip="Import a ClassID Tool patch", triggered=self.importPatch)
        self.exportPatchAct = QtGui.QAction("&Export Patch...", self, statusTip="Export a ClassID Tool patch", triggered=self.exportPatch)

        self.lookupnameAct = QtGui.QAction("&Lookup ClassID Name", self, statusTip="Lookup the name of a ClassID", triggered=self.lookupname)
        self.resetClassIDAct = QtGui.QAction("&Reset ClassID values", self, statusTip="Restore the original ClassID values", triggered=self.resetClassID)

        self.helpAct = QtGui.QAction("&About ClassID Tool", self, statusTip="View information about ClassID Tool", triggered=self.abouttool)

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

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.helpAct)

        self.setWindowTitle("ClassID Tool")

        self.closefile()

        global NameDB
        global PatchOrig
        NameDB = database.readdb(libmisc.programfile_path("NameDatabase"))
        PatchOrig = database.read_patch(libmisc.programfile_path("PatchOriginal"))

    # Define menu action
    def openfile(self):
        global filePath
        filePath = QtGui.QFileDialog.getOpenFileName(self, "Open Overlay0 or NDS ROM", '', "All/Overlay0 Files (*);;NDS ROM (*.nds)")
        filetypeanswer = QtGui.QMessageBox.question(self, "NDS ROM or Overlay0?", "What kind of file is this?\nIf it is an Overlay0, then select the Overlay0 button.\nIf it is a NDS ROM, select the NDS ROM button.", "Cancel", "Overlay0", "NDS ROM")
        global fileType
        if filetypeanswer == 1:
            fileType = "Overlay0"
            self.detectregion()
            self.openAct.setEnabled(False)
            self.closeAct.setEnabled(True)
            self.importPatchAct.setEnabled(True)
            self.exportPatchAct.setEnabled(True)
            self.lookupnameAct.setEnabled(True)
            self.resetClassIDAct.setEnabled(True)
            FileInfoTab.load_info(self.fileInfoTab)
            ClassIDEditingTab.load_file(self.classIDEditingTab)
        elif filetypeanswer == 2:
            ndswarning = QtGui.QMessageBox.warning(self, "NDS ROM Warning!", "The Overlay0 in the NDS ROM MUST be decompressed (ex. by using NSMBe 5.2) in order to read the Overlay0 correctly.\nAre you sure you want to continue?", "&Yes", "&No")
            if ndswarning == 0:
                fileType = "NDS ROM"
                self.detectregion()
                self.openAct.setEnabled(False)
                self.closeAct.setEnabled(True)
                self.importPatchAct.setEnabled(True)
                self.exportPatchAct.setEnabled(True)
                self.lookupnameAct.setEnabled(True)
                self.resetClassIDAct.setEnabled(True)
                global ROMOvOffset
                ROMOvOffset = librom.get_overlay_offset(filePath, ovproc.ovoffset(fileRegion))
                ClassIDEditingTab.load_file(self.classIDEditingTab)
                FileInfoTab.load_info(self.fileInfoTab)

    def closefile(self):
        self.openAct.setEnabled(True)
        self.closeAct.setEnabled(False)
        self.importPatchAct.setEnabled(False)
        self.exportPatchAct.setEnabled(False)
        self.lookupnameAct.setEnabled(False)
        self.resetClassIDAct.setEnabled(False)
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
        choice, ok = QtGui.QInputDialog.getInteger(self, "Lookup ClassID Name", "Specify a ClassID to lookup the name of in the Name Database:", 0, 1, 65536, 1)
        if ok == True:
            Name = File_Interface.NameLookup(choice)
            if Name.upper() == "INVVALUE":
                Name = "not in the Name Database"
            QtGui.QMessageBox.information(self, "ClassID Name Lookup result", ' '.join(["The name of ClassID", str(choice), "is", Name]))

    def abouttool(self):
        QtGui.QMessageBox.about(self, "About ClassID Tool","ClassID Tool\n    By nsmbhacking\nClassID Tool is a tool to modify, read, and lookup names for Class IDs from a NSMB ROM or an extracted Overlay0 from a NSMB ROM.")

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

class FileInfoTab(QtGui.QWidget):
    def __init__(self, parent=None):
        super(FileInfoTab, self).__init__(parent)

        Name_Label_File_Type = QtGui.QLabel("Type: ")
        self.Label_File_Type = QtGui.QLabel("N/A")
        
        Name_Label_ROM_Region = QtGui.QLabel("Region: ")
        self.Label_ROM_Region = QtGui.QLabel("N/A")
        
        Name_Text_File_Path = QtGui.QLabel("File Path: ")
        self.Text_File_Path = QtGui.QLineEdit()
        self.Text_File_Path.setReadOnly(True)

        Name_Text_ROM_OverlayOffset = QtGui.QLabel("ROM Overlay0 Offset: ")
        self.Text_ROM_OverlayOffset = QtGui.QLineEdit()
        self.Text_ROM_OverlayOffset.setReadOnly(True)

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
        self.setLayout(layout)  

    def clear_info(self):
        self.Text_File_Path.setText("N/A")
        self.Text_ROM_OverlayOffset.setText("N/A")
        self.Label_ROM_Region.setText("N/A")
        self.Text_File_Path.setText("N/A")
        self.Label_File_Type.setText("N/A")

    def load_info(self):
        global fileType
        global filePath
        global fileRegion
        global Interface
        self.Label_File_Type.setText(fileType)
        self.Label_ROM_Region.setText(interface.convert_region(fileRegion))
        self.Text_File_Path.setText(filePath)
        if fileType == "NDS ROM":
            global ROMOvOffset
            self.Text_ROM_OverlayOffset.setText(str(ROMOvOffset))

class ClassIDEditingTab(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ClassIDEditingTab, self).__init__(parent)

        self.classidTable = QtGui.QTableWidget(0, 2)

        self.classidTable.setHorizontalHeaderLabels(("ClassID Name", "ClassID #"))
        self.classidTable.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.classidTable.setShowGrid(True)
        self.classidTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.classidTable.cellActivated.connect(self.editclassid)
        
        self.Layout = QtGui.QGridLayout()
        self.Layout.addWidget(self.classidTable, 0, 0)
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
        currentSprite = self.classidTable.currentRow() + 1
        choice, ok = QtGui.QInputDialog.getInteger(self, "Change ClassID", ' '.join(["Change ClassID of Sprite", str(currentSprite), "to:"]), 0, 1, 65536, 1)
        if ok == True:
            File_Interface.ClassIDWrite(currentSprite, choice)
            ClassIDTableName = File_Interface.NameLookup(File_Interface.ClassIDRead(choice))
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

filePath = None
fileType = None
fileRegion = None
ROMOvOffset = None
NameDB = None
PatchOrig = None

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    Interface = interface()
    Interface.show()

    sys.exit(app.exec_())
