import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication , QMainWindow,QFileDialog

Form = uic.loadUiType(os.path.join(os.getcwd(),"mainForm.ui"))[0]

class mainWindow(QMainWindow, Form):
    def __init__(self):
        super(mainWindow,self).__init__()
        self.setupUi(self)
        self.addInDir.clicked.connect(self.addNewDir)
        self.delDir_pb.clicked.connect(self.delDir)

    def addNewDir(self):
        directory=str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        for i in range(self.inDirs_lw.count()):
            #print(f"Here {i}")
            #print(self.inDirs_lw.item(i).text())
            if str(self.inDirs_lw.item(i).text())== directory:
                return
                #print("HERE")
        self.inDirs_lw.addItem(directory)

    def delDir(self):
        if(self.inDirs_lw.currentItem() != None):
            self.inDirs_lw.takeItem(self.inDirs_lw.currentRow())
            #print(self.inDirs_lw.currentItem().text())

app = QApplication(sys.argv)
#app.setStyle("Fusion")

window= mainWindow()
window.show()

sys.exit(app.exec())