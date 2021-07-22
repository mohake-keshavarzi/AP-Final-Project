import sys
import os
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtWidgets import QApplication , QMainWindow,QFileDialog , QTableWidgetItem,QGraphicsScene,QErrorMessage


Form = uic.loadUiType(os.path.join(os.getcwd(),"mainForm.ui"))[0]

class mainWindow(QMainWindow, Form):
    def __init__(self):
        super(mainWindow,self).__init__()
        self.setupUi(self)
        self.addInDir.clicked.connect(self.addNewDir)
        self.delDir_pb.clicked.connect(self.delDir)
        self.outDir_le.setText(os.getcwd())
        self.outDir_pb.clicked.connect(self.outDir)
        self.imgNames_tw.cellClicked.connect(self.showImg)
        self.scene=QGraphicsScene()
        #self.scene.addText("Hello")
        self.graphView_gv.setScene(self.scene)
        self.myImg

    def addNewDir(self):
        directory=str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        for i in range(self.inDirs_lw.count()):
            #print(f"Here {i}")
            #print(self.inDirs_lw.item(i).text())
            if str(self.inDirs_lw.item(i).text())== directory:
                return
                #print("HERE")
        if directory!='':
            self.inDirs_lw.addItem(directory)
            self.collectImgs(directory)


    def delDir(self):
        if(self.inDirs_lw.currentItem() != None):
            dirtext=self.inDirs_lw.currentItem().text()
            self.inDirs_lw.takeItem(self.inDirs_lw.currentRow())
            #print(self.imgNames_tw.rowCount())
            i=0
            for j in range(self.imgNames_tw.rowCount()):
                if self.imgNames_tw.item(i,1)==None:
                    break
                #print(dirtext)
                #print(self.imgNames_tw.item(i,1).text())
                if self.imgNames_tw.item(i,1).text()== os.path.join(dirtext, (self.imgNames_tw.item(i,0).text())) :
                    #print("deleted")
                    self.imgNames_tw.removeRow(i)
                    i=i-1
                i=i+1
            #print(self.inDirs_lw.currentItem().text())

    def outDir(self):
        directory=str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        #self.outDir_le.setText("dddddddddddQQQQQQQ")
        if directory != "":
            self.outDir_le.setText(directory)

    def collectImgs(self,folder):
        with os.scandir(folder) as it:
            i=self.imgNames_tw.rowCount()
            for entry in it:
                if (entry.name.endswith('.png') or entry.name.endswith('.PNG') or entry.name.endswith('.jpg') or entry.name.endswith('.JPG') or entry.name.endswith('.jpeg') or entry.name.endswith('.JPEG')) and entry.is_file():
                    #print(entry.name)
                    #self.imgNames_lw.addItem(entry.name)
                    self.imgNames_tw.insertRow(i)
                    tumb=QTableWidgetItem(QtGui.QIcon(entry.path),entry.name)
                    self.imgNames_tw.setItem(i,0,tumb)
                    self.imgNames_tw.setItem(i,1,QTableWidgetItem(entry.path))
                    
                    
                    i=i+1
    
    def showImg(self,row,col):
        #self.scene.addText(f'{row},{col}')
        pix=QtGui.QPixmap()
        try:
            pix.load(self.imgNames_tw.item(row,1).text())
            self.scene.clear()
            pixit=self.scene.addPixmap(pix)
            self.graphView_gv.fitInView(pixit,QtCore.Qt.KeepAspectRatio)
        except:
            err=QErrorMessage(self)
            err.showMessage("Something went wrong! Maybe the image is deleted or moved")
                    


app = QApplication(sys.argv)
#app.setStyle("Fusion")

window= mainWindow()
window.show()

sys.exit(app.exec())