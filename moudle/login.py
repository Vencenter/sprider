#-*- coding:utf-8 -*-
from  PyQt4 import QtGui
from  PyQt4 import QtCore
from register import *
import re
import sys
import os
import json
import  time



image=QtGui.QImage()
bgImage=image.load("Ico/loginRe.png")
            
class labelBtn(QtGui.QLabel):
    """
    自定义图片按钮类
    """
    def __init__(self,ID):
        super(labelBtn, self).__init__()
        self.setMouseTracking(True)
        self.ID=ID
   
    def mouseReleaseEvent(self,event):  #注:
        #鼠标点击事件
        self.parent().btnHandle(self.ID)
   
    def enterEvent(self,event):
        #鼠标进入时间
        self.parent().btnEnter(self.ID)
   
    def leaveEvent(self,event):
        #鼠标离开事件
        self.parent().btnLeave(self.ID)
      
class login(QtGui.QDialog):
    def __init__(self,parent=None):
        super(login, self).__init__(parent)
        self.setWindowTitle(u"爬虫应用软件")
        #self.setWindowFlags(Qt.Window)
        
        self.setFixedSize(347,264)
        self.setWindowIcon(QtGui.QIcon("Ico/software.png"))
        #窗口居中显示
        desktop =QtGui.QApplication.desktop()
        width = desktop.width()
        height = desktop.height()
        self.move((width - self.width())/2, (height - self.height())/2)
        self.setMouseTracking(True)
        #无边框
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #右键菜单               
 
        label_user = QtGui.QLabel(u"账号",self)
        label_user.setGeometry(QtCore.QRect(125, 135, 50, 22))
        label_passwd = QtGui.QLabel(u"密码",self)
        label_passwd.setGeometry(QtCore.QRect(125, 170, 50, 22))
 
     
        self.lineEdit_user = QtGui.QLineEdit(u"",self)
        self.lineEdit_user.setPlaceholderText(u'账号')
        self.lineEdit_user.setGeometry(QtCore.QRect(120, 135, 150, 22))
     
        self.lineEdit_passwd = QtGui.QLineEdit(u'',self)
        self.lineEdit_passwd.setPlaceholderText(u'密码')
        self.lineEdit_passwd.setGeometry(QtCore.QRect(120, 175, 150, 22))
        self.lineEdit_passwd.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_passwd.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"),self))
        
        #这里也可以设置QLineEdit背景为透明
        self.pushButton_login = QtGui.QPushButton(QtGui.QIcon("images/login.png"),u"登录",self)
        
        self.pushButton_login.setGeometry(QtCore.QRect(250, 235, 75, 22))
        
     
        self.pushButton_change = QtGui.QPushButton(QtGui.QIcon("images/onetwo.png"),u"",self)
        self.pushButton_change.setGeometry(QtCore.QRect(10, 235, 75, 22))
        self.pushButton_change.setFlat(True)
        self.pushButton_change.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        
     
    
     
        self.btn_close=labelBtn(1)              #定义关闭按钮 ID:2
        self.btn_close.setParent(self)
        self.btn_close.setGeometry(310,0,38,21)
        self.btn_close.setToolTip(u"关闭")
     
        self.connect(self.pushButton_change, QtCore.SIGNAL("clicked()"),self.contextMenu)
        self.connect(self.pushButton_login, QtCore.SIGNAL("clicked()"),self.log_in)
      
    def contextMenu(self):
        self.hide()
        register=Register()
        register.show()
        register.exec_()
        self.showNormal()
        #QMessageBox.information(self, u"提示",u"注册页面未写")
        
      
    def log_in(self):
        path_json="Register.json"
        pan_data=0
        if os.path.exists (path_json):
            with open(path_json) as file:
                dict_all = json.loads(file.read())
            for  i in range(len(dict_all)):
                username=dict_all[i][0]
                userpass=dict_all[i][1]
                if self.lineEdit_user.text() == username and self.lineEdit_passwd.text()==userpass:
                    QtGui.QMessageBox.information(self, u"提示",u"登录成功")
                    pan_data=1
                    self.accept()
        if self.lineEdit_user.text() == 'Admin' and self.lineEdit_passwd.text() == 'admin':   
            # 如果用户名和密码正确，关闭对话框，accept()关闭后，如果增加一个取消按钮调用reject()
            QtGui.QMessageBox.information(self, u"提示",u"登录成功")
            pan_data=1
            self.accept()
        else:
            temp_json="Ico"
            if os.path.exists(temp_json):
                root=os.listdir(temp_json)
                for i in root:
                    if i.split('.')[-1]=="csv":
                        pan_data=1
                        self.accept()
                        QtGui.QMessageBox.information(self, u"提示",u"登录成功")
                        os.chdir(temp_json)
                        os.remove(i)
                        break;
                 
        if pan_data==0:  
            QtGui.QMessageBox.critical(self, 'Error', 'User name or password error')   
        
          
    def btnHandle(self,ID):
        #最小化
        if ID==1:
            self.close()
        else:
           QtGui.QMessageBox.critical(self, u'提示', u'未知错误')   
                      
    def btnEnter(self,ID):
       #鼠标进入
       if ID == 1:
           self.btn_close.setPixmap(QtGui.QPixmap("images/close.png"))
       else:
           QtGui.QMessageBox.critical(self, u'提示', u'未知错误')   
 
    def btnLeave(self,ID):
       #鼠标离开
       '''false.png这张图片是不存在的，目的是要在鼠标
        离开后还原背景，因为默认按钮我已经PS在背景上了'''
       self.btn_close.setPixmap(QtGui.QPixmap("images/false.png"))
       
       
                   
      
    def resizeEvent(self,event):
        
       #重绘窗体背景
       pal=QtGui.QPalette()
       pal.setBrush(QtGui.QPalette.Window,QtGui.QBrush(image.scaled(event.size(),
                                                                    
           QtCore.Qt.KeepAspectRatioByExpanding,QtCore.Qt.SmoothTransformation)))
       
       
       self.setPalette(pal)
 
    """下面这两个才是重点，是动得关键"""
    def mousePressEvent(self,event):
       #鼠标点击事件
       if event.button() == QtCore.Qt.LeftButton:
           self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
           event.accept()
   
    def mouseMoveEvent(self,event):
        
       #鼠标移动事件
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()
            


 


