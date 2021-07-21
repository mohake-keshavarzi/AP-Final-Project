import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication , QMainWindow

Form = uic.loadUiType(os.path.join(os.getcwd(),"mainForm.ui"))[0]

class mainWindow(QMainWindow, Form):
    def __init__(self):
        super(mainWindow,self).__init__()
        self.setupUi(self)

app = QApplication(sys.argv)
#app.setStyle("Fusion")

window= mainWindow()
window.show()

sys.exit(app.exec())