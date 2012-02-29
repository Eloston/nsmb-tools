from PyQt4 import QtCore, QtGui
import libbnbl
import mmap

class Interface(QtGui.QMainWindow):
    def __init__(self):
        super(Interface, self).__init__()

        self.editorver = "2.1"

        self.bnblFile = None

        self.newAct = QtGui.QAction("&New", self, statusTip="", triggered=self.newfile)
        self.openAct = QtGui.QAction("&Open", self, statusTip="", triggered=self.openfile)
        self.closeAct = QtGui.QAction("&Close", self, statusTip="", triggered=self.closefile)
        self.saveAct = QtGui.QAction("&Save", self, statusTip="", triggered=self.savefile)
        self.exitAct = QtGui.QAction("&Exit", self, statusTip="", triggered=self.close)

        self.repairindexAct = QtGui.QAction("By &Index value", self, statusTip="", triggered=self.repairindex)
        self.repairnonindexAct = QtGui.QAction("By &Number of Touch Regions", self, statusTip="", triggered=self.repairnonindex)

        self.aboutAct = QtGui.QAction(' '.join(["&About BNBL Editor", self.editorver]), self, statusTip="", triggered=self.aboutprogram)

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.closeAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addSeparator()
        self.repairMenu = self.fileMenu.addMenu("&Repair")
        self.repairMenu.addAction(self.repairindexAct)
        self.repairMenu.addAction(self.repairnonindexAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)

        self.touchregionTable = QtGui.QTableWidget(0, 4)

        self.closeAct.setEnabled(False)
        self.saveAct.setEnabled(False)

        self.touchregionTable.setHorizontalHeaderLabels(("X", "Y", "Width", "Height"))
        self.touchregionTable.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.touchregionTable.setShowGrid(True)
        #self.classidTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        #self.classidTable.cellActivated.connect(self.asdf)

        Name_bnblPathBox = QtGui.QLabel("BNBL File Path: ")
        self.bnblPathBox = QtGui.QLineEdit()
        self.bnblPathBox.setReadOnly(True)
        
        self.Layout_bnblPathBox = QtGui.QGridLayout()
        self.Layout_bnblPathBox.addWidget(Name_bnblPathBox, 0, 0)
        self.Layout_bnblPathBox.addWidget(self.bnblPathBox, 0, 1)

        self.addtablerowbutton = QtGui.QPushButton("Add a row")
        self.addtablerowbutton.clicked.connect(self.addtablerow)
        self.removetablerowbutton = QtGui.QPushButton("Remove a row")
        self.removetablerowbutton.clicked.connect(self.removetablerow)
        self.duplicatetablerowbutton = QtGui.QPushButton("Duplicate a row")
        self.duplicatetablerowbutton.clicked.connect(self.duplicatetablerow)

        self.addtablerowbutton.setEnabled(False)
        self.removetablerowbutton.setEnabled(False)
        self.duplicatetablerowbutton.setEnabled(False)

        self.Layout_bottom = QtGui.QGridLayout()
        self.Layout_bottom.addWidget(self.addtablerowbutton, 0, 0)
        self.Layout_bottom.addWidget(self.removetablerowbutton, 0, 1)
        self.Layout_bottom.addWidget(self.duplicatetablerowbutton, 0, 2)

        self.Layout = QtGui.QGridLayout()
        self.Layout.addLayout(self.Layout_bnblPathBox, 0, 0)
        self.Layout.addWidget(self.touchregionTable, 1, 0)
        self.Layout.addLayout(self.Layout_bottom, 2, 0)

        self.loadLayout = QtGui.QWidget()
        self.loadLayout.setLayout(self.Layout)
        self.setCentralWidget(self.loadLayout)

        self.setWindowTitle(' '.join(["BNBL Editor", self.editorver]))

        #self.touchregionTable.cellDoubleClicked.connect(self.newfile)

    def newfile(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self, "Create a new bnbl file", '', "bnbl Files (*.bnbl);;All Files (*)")
        if fileName:
            try:
                FILE = open(fileName, mode="wb")
            except:
                QtGui.QMessageBox.critical(self, "Error while creating bnbl file", "Unable to create file!\nCould be caused by an invalid path, or access permissions.", "OK")
                return None
            FILE.write(b'JNBL\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00')
            FILE.close()
            self.bnblPath = fileName
            self.openfile(True)

    def openfile(self, SKIPDIALOG=False):
        if not SKIPDIALOG:
            self.bnblPath = QtGui.QFileDialog.getOpenFileName(self, "Choose a bnbl file to open", '', "bnbl Files (*.bnbl);;All Files (*)")
        if not self.bnblPath == '':
            self.bnblFile = open(self.bnblPath, mode='r+b')
            self.bnblFile = mmap.mmap(self.bnblFile.fileno(), 0)
            if libbnbl.verify_bnbl_header(self.bnblFile):
                self.bnblPathBox.setText(self.bnblPath)
                self.closeAct.setEnabled(True)
                self.openAct.setEnabled(False)
                self.saveAct.setEnabled(True)
                self.newAct.setEnabled(False)
                self.repairMenu.setEnabled(False)
                self.addtablerowbutton.setEnabled(True)
                self.removetablerowbutton.setEnabled(True)
                self.duplicatetablerowbutton.setEnabled(True)
                self.populatetable()
            else:
                self.bnblFile.close()
                QtGui.QMessageBox.critical(self, "Invalid BNBL Header", "The header of the BNBL file is invalid.", "OK")

    def closefile(self):
        self.bnblFile.close()
        self.bnblFile = None
        self.bnblPath = ''
        self.bnblPathBox.setText(self.bnblPath)
        self.closeAct.setEnabled(False)
        self.openAct.setEnabled(True)
        self.saveAct.setEnabled(False)
        self.newAct.setEnabled(True)
        self.repairMenu.setEnabled(True)
        self.addtablerowbutton.setEnabled(False)
        self.removetablerowbutton.setEnabled(False)
        self.duplicatetablerowbutton.setEnabled(False)
        self.cleartable()

    def savefile(self):
        self.writetable2buffer()
        self.bnblFile.flush()

    def repairindex(self):
        self.repairfile(True)

    def repairnonindex(self):
        self.repairfile(False)

    def repairfile(self, TYPE):
        bnblPath = QtGui.QFileDialog.getOpenFileName(self, "Choose a bnbl file to repair", '', "bnbl Files (*.bnbl);;All Files (*)")
        if not bnblPath == '':
            bnblFile = open(bnblPath, mode='r+b')
            bnblFile = mmap.mmap(bnblFile.fileno(), 0)
            if libbnbl.verify_bnbl_header(bnblFile):
                libbnbl.repairbnbl(bnblFile, TYPE)
                bnblFile.close()
                openbnblanswer = QtGui.QMessageBox.question(self, "Open repaired bnbl?", "The bnbl was repaired by the index value sucessfully.\nWould you like to open it?", "Yes", "No")
                if openbnblanswer == 0:
                    self.bnblPath = bnblPath
                    self.openfile(True)
            else:
                bnblFile.close()
                QtGui.QMessageBox.critical(self, "Invalid BNBL Header", "The header of the BNBL file is invalid.", "OK")

    def populatetable(self):
        MAX = libbnbl.num_touchregions(self.bnblFile, [False])
        ROWS = 0
        while ROWS <= MAX:
            DATA = libbnbl.touchregions(self.bnblFile, [False, ROWS])

            touchregionX = QtGui.QSpinBox()
            touchregionX.setRange(0, 255)
            touchregionX.setValue(DATA[0])

            touchregionY = QtGui.QSpinBox()
            touchregionY.setRange(0, 255)
            touchregionY.setValue(DATA[1])

            touchregionWidth = QtGui.QSpinBox()
            touchregionWidth.setRange(0, 255)
            touchregionWidth.setValue(DATA[2])

            touchregionHeight = QtGui.QSpinBox()
            touchregionHeight.setRange(0, 255)
            touchregionHeight.setValue(DATA[3])

            self.touchregionTable.insertRow(ROWS)
            self.touchregionTable.setCellWidget(ROWS, 0, touchregionX)
            self.touchregionTable.setCellWidget(ROWS, 1, touchregionY)
            self.touchregionTable.setCellWidget(ROWS, 2, touchregionWidth)
            self.touchregionTable.setCellWidget(ROWS, 3, touchregionHeight)
            ROWS = ROWS + 1
    def cleartable(self):
        self.touchregionTable.clearContents()
        self.touchregionTable.setRowCount(0)
    def writetable2buffer(self):
        MAX = libbnbl.num_touchregions(self.bnblFile, [False])
        ROWS = 0
        while ROWS <= MAX:
            touchregionX = libbnbl.compute_xy_cord(self.touchregionTable.cellWidget(ROWS, 0).value())
            touchregionY = libbnbl.compute_xy_cord(self.touchregionTable.cellWidget(ROWS, 1).value())
            touchregionWidth = self.touchregionTable.cellWidget(ROWS, 2).value()
            touchregionHeight = self.touchregionTable.cellWidget(ROWS, 3).value()
            libbnbl.touchregions(self.bnblFile, [True, ROWS, [touchregionX[0], touchregionX[1], touchregionY[0], touchregionY[1], touchregionWidth, touchregionHeight]])
            ROWS = ROWS + 1

    def addtablerow(self):
        choice, ok = QtGui.QInputDialog.getInteger(self, "Add row", "Specify the new row number:", 0, 1, libbnbl.num_touchregions(self.bnblFile, [False])+1, 1)
        if ok:
            choice = choice - 1
            blah1 = QtGui.QSpinBox()
            blah1.setRange(0, 255)
            blah2 = QtGui.QSpinBox()
            blah2.setRange(0, 255)
            blah3 = QtGui.QSpinBox()
            blah3.setRange(0, 255)
            blah4 = QtGui.QSpinBox()
            blah4.setRange(0, 255)
            self.touchregionTable.insertRow(choice)
            self.touchregionTable.setCellWidget(choice, 0, blah1)
            self.touchregionTable.setCellWidget(choice, 1, blah2)
            self.touchregionTable.setCellWidget(choice, 2, blah3)
            self.touchregionTable.setCellWidget(choice, 3, blah4)
            libbnbl.addremove_touchregions(self.bnblFile, [True, 1])
            self.bnblFile.flush()

    def removetablerow(self):
        choice, ok = QtGui.QInputDialog.getInteger(self, "Remove row", "Specify a row to remove:", 0, 1, libbnbl.num_touchregions(self.bnblFile, [False])+1, 1)
        if ok:
            choice = choice - 1
            libbnbl.addremove_touchregions(self.bnblFile, [False, choice])
            self.bnblFile.flush()
            self.touchregionTable.removeRow(choice)

    def duplicatetablerow(self):
        original, ok = QtGui.QInputDialog.getInteger(self, "Duplicate row", "Specify a row to duplicate:", 0, 1, libbnbl.num_touchregions(self.bnblFile, [False])+1, 1)
        if ok:
            new, ok = QtGui.QInputDialog.getInteger(self, "Duplicate row", "Specify a location for the duplicate row:", 0, 1, libbnbl.num_touchregions(self.bnblFile, [False])+1, 1)
            if ok:
                original = original - 1
                new = new - 1
                blah1 = QtGui.QSpinBox()
                blah1.setRange(0, 255)
                blah1.setValue(self.touchregionTable.cellWidget(original, 0).value())
                blah2 = QtGui.QSpinBox()
                blah2.setRange(0, 255)
                blah2.setValue(self.touchregionTable.cellWidget(original, 1).value())
                blah3 = QtGui.QSpinBox()
                blah3.setRange(0, 255)
                blah3.setValue(self.touchregionTable.cellWidget(original, 2).value())
                blah4 = QtGui.QSpinBox()
                blah4.setRange(0, 255)
                blah4.setValue(self.touchregionTable.cellWidget(original, 3).value())
                self.touchregionTable.insertRow(new)
                self.touchregionTable.setCellWidget(new, 0, blah1)
                self.touchregionTable.setCellWidget(new, 1, blah2)
                self.touchregionTable.setCellWidget(new, 2, blah3)
                self.touchregionTable.setCellWidget(new, 3, blah4)
                libbnbl.addremove_touchregions(self.bnblFile, [True, 1])
                self.bnblFile.flush()

    def aboutprogram(self):
        QtGui.QMessageBox.about(self, ' '.join(["About BNBL Editor", self.editorver]),"BNBL Editor\n    By ELMario\n    Specifications by ray\n\nBNBL Editor is a tool to easily modify BNBL files.")

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    interface = Interface()
    interface.show()

    sys.exit(app.exec_())
