import sys
import os
import opncvAP
import temp
import cv2
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtWidgets import QApplication , QMainWindow,QFileDialog , QTableWidgetItem,QGraphicsScene,QErrorMessage,QMessageBox


Form = uic.loadUiType(os.path.join(os.getcwd(),"mainForm.ui"))[0]

class mainWindow(QMainWindow, Form):
    def __init__(self):
        super(mainWindow,self).__init__()
        self.setupUi(self)
        self.addInDir.clicked.connect(self.addNewDir)
        self.delDir_pb.clicked.connect(self.delDir)
        self.outDir_le.setText(os.getcwd())
        self.outDir_le.setText(os.path.join(os.getcwd(),"images2"))
        # self.outDir_pb.clicked.connect(self.outDir)
        self.imgNames_tw.cellClicked.connect(self.showImg)
        self.scene=QGraphicsScene()
        #self.scene.addText("Hello")
        self.graphView_gv.setScene(self.scene)
        #self.myImg
        self.myCVimg=None
        self.myCVimg_backup=None
        self.nextImg=None
        self.grayScale_pb.clicked.connect(self.makeGray)
        self.rotate_dial.valueChanged.connect(self.doRotate)
        self.confRot_pb.clicked.connect(self.confirmRotation)
        self.blur_sb.valueChanged.connect(self.doBlur)
        self.confBlur_pb.clicked.connect(self.confirmBlur)
        self.x_sb.valueChanged.connect(self.doResize)
        self.y_sb.valueChanged.connect(self.doResize)
        self.cx_sb.valueChanged.connect(self.doCrop)
        self.cy_sb.valueChanged.connect(self.doCrop)
        self.cw_sb.valueChanged.connect(self.doCrop)
        self.ch_sb.valueChanged.connect(self.doCrop)
        self.confRsz_pb.clicked.connect(self.confirmResize)
        self.confCrp_pb.clicked.connect(self.confirmCrop)
        self.showmeRndCrp_pb.clicked.connect(self.doRandomCrop)
        self.confRndCrp_pb.clicked.connect(self.confirmRandomCrop)
        self.tasksList=[]
        self.kval=0
        self.x1val=0
        self.x2val=0
        self.y1val=0
        self.y2val=0
        self.doAll_pb.clicked.connect(self.doAlltasksForAll)
        self.upload_pb.clicked.connect(lambda: temp.uploadAll())
        # self.ch_pb.clicked.connect(lambda: print(self.tasksList))
        

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

    # def outDir(self):
    #     directory=str(QFileDialog.getExistingDirectory(self, "Select Directory"))
    #     #self.outDir_le.setText("dddddddddddQQQQQQQ")
    #     if directory != "":
    #         self.outDir_le.setText(directory)

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
            self.myCVimg=opncvAP.read_image(self.imgNames_tw.item(row,1).text())
            self.myCVimg_backup=self.myCVimg
            pix.load(self.imgNames_tw.item(row,1).text())
            self.scene.clear()
            pixit=self.scene.addPixmap(pix)
            self.graphView_gv.fitInView(pixit,QtCore.Qt.KeepAspectRatio)
        except:
            err=QErrorMessage(self)
            err.showMessage("Something went wrong! Maybe the image is deleted or moved")
                    
    def redrawImg(self,img):
        self.scene.clear()
        pix=opncvAP.convert_cv_qt(img)
        pixit=self.scene.addPixmap(pix)
        self.graphView_gv.fitInView(pixit,QtCore.Qt.KeepAspectRatio)
        # cvRGBImg = cv2.cvtColor(self.myCVimg, cv2.COLOR_BGR2RGBA)
        # x = cvRGBImg.shape[1]
        # y = cvRGBImg.shape[0]
        # qimg = QtGui.QImage(cvRGBImg,x,y, QtGui.QImage.Format_RGB32)
        # #helpy=opncvAP.cv2_to_Qimg(self.myCVimg)
        # pix=QtGui.QPixmap.fromImage(qimg)
        # pixit=self.scene.addPixmap(pix)
        #print("5")
        #self.graphView_gv.fitInView(pixit,QtCore.Qt.KeepAspectRatio)
    
    def makeGray(self):
        
        newImg=opncvAP.gray_scale(self.myCVimg)
        if newImg is None:
            return
        else:
            self.myCVimg=newImg
            self.redrawImg(self.myCVimg)
            self.tasksList.append("GrayScale")
            self.doneTasks_lw.addItem("GrayScale")

    def doRotate(self):
        
        #self.myCVimg
        newImg=opncvAP.rotate(self.myCVimg, self.rotate_dial.value())
        self.rotate_lb.setText(f"{self.rotate_dial.value()} degree")
        self.redrawImg(newImg)
        self.nextImg=newImg
        #self.rotate_dial.value()]
        

    def confirmRotation(self):
        
        
        if self.nextImg is None or self.rotate_dial.value()==0:
            return
        else:
            self.myCVimg=self.nextImg
            self.doneTasks_lw.addItem(f"Rotated to {self.rotate_dial.value()} degree")
            self.tasksList.append(("Rotate",self.rotate_dial.value() ))

            self.nextImg=None
            self.rotate_dial.setValue(0)
            self.rotate_lb.setText(f"{self.rotate_dial.value()} degree")
            self.redrawImg(self.myCVimg)
            
            

    def doBlur(self):
        
        if self.blur_sb.value()> min(self.myCVimg.shape[0],self.myCVimg.shape[1]):
            k=min(self.myCVimg.shape[0],self.myCVimg.shape[1])
            self.blur_sb.setValue(k)
        else:
            k=self.blur_sb.value()
        newImg=opncvAP.blur(self.myCVimg, k)
        self.kval=k
        self.redrawImg(newImg)
        self.nextImg=newImg
        

    def confirmBlur(self):

        if self.nextImg is None or self.blur_sb.value()==0:
            return
        else:
            self.myCVimg=self.nextImg
            self.nextImg=None
            self.tasksList.append(("Blur",self.kval))
            self.doneTasks_lw.addItem(f"Blur to {self.kval}")
            self.blur_sb.setValue(1)
            # self.rotate_lb.setText(f"{self.rotate_dial.value()} degree")
            self.redrawImg(self.myCVimg)
            
            

    def doResize(self):

        newImg=opncvAP.resize(self.myCVimg, self.x_sb.value(), self.y_sb.value())
        self.redrawImg(newImg)
        self.nextImg=newImg

    def confirmResize(self):
        if self.nextImg is None:
            return
        else:
            self.myCVimg=self.nextImg
            self.doneTasks_lw.addItem(f"Resized to X={self.x_sb.value()} , Y={self.y_sb.value()} ")
            self.tasksList.append(("Resize",self.x_sb.value(),self.y_sb.value()))
            self.nextImg=None
            self.x_sb.setValue(1)
            self.y_sb.setValue(1)
            # self.rotate_lb.setText(f"{self.rotate_dial.value()} degree")
            self.redrawImg(self.myCVimg)

            

    def doCrop(self):
        x1=self.cx_sb.value()
        y1=self.cy_sb.value()

        x2=x1+self.cw_sb.value()
        y2=y1+self.ch_sb.value()
        
        if(x2>self.myCVimg.shape[1]):
            x2=self.myCVimg.shape[1]
        
        if(y2>self.myCVimg.shape[0]):
            y2=self.myCVimg.shape[0]
        self.x1val=x1
        self.x2val=x2
        self.y1val=y1
        self.y2val=y2        
        newImg=opncvAP.crop(self.myCVimg, x1, y1, x2, y2)
        self.redrawImg(newImg)
        self.nextImg=newImg

    def confirmCrop(self):
        if self.nextImg is None:
            return
        else:
            self.myCVimg=self.nextImg
            self.doneTasks_lw.addItem(f"Crop to x1={self.x1val} y1={self.y1val} x2={self.y2val} y2={self.y2val}")
            self.tasksList.append(("Crop",self.x1val,self.y1val,self.x2val,self.y2val))
            self.nextImg=None
            self.cx_sb.setValue(0)
            self.cy_sb.setValue(0)
            self.cw_sb.setValue(1)
            self.ch_sb.setValue(1)
            self.redrawImg(self.myCVimg)

    def doRandomCrop(self):
        
        newImg=opncvAP.random_crop(self.myCVimg)
        self.redrawImg(newImg)
        self.nextImg=newImg
        

    def confirmRandomCrop(self):
        if self.nextImg is None:
            return
        else:
            self.myCVimg=self.nextImg
            self.doneTasks_lw.addItem("RandomCrop")
            self.tasksList.append(("RandomCrop",0))
            self.nextImg=None
            
            self.redrawImg(self.myCVimg)

    def doAlltasksForAll(self):
        cv2img=None
        for i in range(self.imgNames_tw.rowCount()):
            cv2img=opncvAP.read_image(self.imgNames_tw.item(i,1).text())
            for tsk in self.tasksList:
                if tsk[0]=="GrayScale":
                    try:
                        cv2img=opncvAP.gray_scale(cv2img)
                        print(f"{self.imgNames_tw.item(i,1).text()} GrayScale Passed!")
                    except:
                        print(f"{self.imgNames_tw.item(i,1).text()} GrayScale Failed")
                if tsk[0]=="Rotate":
                    try:
                        cv2img=opncvAP.rotate(cv2img, tsk[1])
                        print(f"{self.imgNames_tw.item(i,1).text()} Rotate Passed!")
                    except:
                        print(f"{self.imgNames_tw.item(i,1).text()} Rotate Failed")
                if tsk[0]=="Blur":
                    try:
                        cv2img=opncvAP.blur(cv2img, tsk[1])
                        print(f"{self.imgNames_tw.item(i,1).text()} Blur Passed!")
                    except:
                        print(f"{self.imgNames_tw.item(i,1).text()} Blur Failed")
                if tsk[0]=="Resize":
                    try:
                        cv2img=opncvAP.resize(cv2img, tsk[1], tsk[2])
                        print(f"{self.imgNames_tw.item(i,1).text()} Resize Passed!")
                    except:
                        print(f"{self.imgNames_tw.item(i,1).text()} Resize Failed")
                if tsk[0]=="Crop":
                    try:
                        cv2img=opncvAP.crop(cv2img, tsk[1], tsk[2], tsk[3], tsk[4])
                        print(f"{self.imgNames_tw.item(i,1).text()} Crop Passed!")
                    except:
                        print(f"{self.imgNames_tw.item(i,1).text()} Crop Failed")
                if tsk[0]=="RandomCrop":
                    try:
                        cv2img=opncvAP.random_crop(cv2img)
                        print(f"{self.imgNames_tw.item(i,1).text()} RandomCrop Passed!")
                    except:
                        print(f"{self.imgNames_tw.item(i,1).text()} RandomCrop Failed")
            
            opncvAP.save_im(f"{self.outDir_le.text()}\{self.imgNames_tw.item(i,0).text()}" , cv2img)
        



   
        

app = QApplication(sys.argv)
#app.setStyle("Fusion")

window= mainWindow()
window.show()

sys.exit(app.exec())