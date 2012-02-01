# NSMBe Sprite Data Updater

from PyQt4 import QtCore, QtGui
import urllib.request
import os.path

class interface(QtGui.QWidget):
    def __init__(self):
        super(interface, self).__init__()

        Name_downloaddirectorybox = QtGui.QLabel("Spritedata download path:")
        self.downloaddirectorybox = QtGui.QLineEdit()
        self.updatedownloadlocationbutton = QtGui.QPushButton("Update")
        self.updatedownloadlocationbutton.show()
        self.updatedownloadlocationbutton.clicked.connect(self.updatedownloadlocation)

        self.downloadlocationbutton = QtGui.QPushButton("Choose Download Location")
        self.downloadlocationbutton.show()
        self.downloadlocationbutton.clicked.connect(self.downloadlocation)

        self.downloadspritedatabutton = QtGui.QPushButton("Download Spritedata.txt to location")
        self.downloadspritedatabutton.show()
        self.downloadspritedatabutton.clicked.connect(self.downloadspritedata)

        self.Layoutdirectorypath = QtGui.QGridLayout()
        self.Layoutdirectorypath.addWidget(Name_downloaddirectorybox, 0, 0)
        self.Layoutdirectorypath.addWidget(self.downloaddirectorybox, 0, 1)
        self.Layoutdirectorypath.addWidget(self.updatedownloadlocationbutton, 0, 2)

        self.Layout = QtGui.QGridLayout()
        self.Layout.addLayout(self.Layoutdirectorypath, 0, 0)
        self.Layout.addWidget(self.downloadlocationbutton, 1, 0)
        self.Layout.addWidget(self.downloadspritedatabutton, 2, 0)
        self.setLayout(self.Layout)

        self.setWindowTitle("NSMBe Spritedata Downloader")

    def downloadlocation(self):
        options = QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self, "Find NSMBe's directory", '', options)
        if directory:
            global DownloadLocation
            DownloadLocation = directory
            self.downloaddirectorybox.setText(directory)

    def downloadspritedata(self):
        try:
            RequestSpritedata = urllib.request.urlopen("http://nsmbhd.net/spritedata.php")
        except:
            FILE.close()
            QtGui.QMessageBox.critical(self, "Error while downloading", "Unable to download new Spritedata!", "OK")
            return None
        try:
            FILE = open(os.path.join(DownloadLocation, "spritedata.txt"), mode="wb")
        except:
            QtGui.QMessageBox.critical(self, "Error while downloading", "Unable to create file!\nCould be caused by an invalid path, or access permissions.", "OK")
            return None
            
        NewSpritedata = RequestSpritedata.read()
        RequestSpritedata.close()
        FILE.write(NewSpritedata)
        QtGui.QMessageBox.information(self, "Operation complete!", "The spritedata has been updated sucessfully.")

    def updatedownloadlocation(self):
        global DownloadLocation
        DownloadLocation = self.downloaddirectorybox.text()

DownloadLocation = ''

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    Interface = interface()
    Interface.show()

    sys.exit(app.exec_())
