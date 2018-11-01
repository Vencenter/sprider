#-*- coding:utf-8 -*-
from  PyQt4 import QtGui
from  PyQt4 import QtCore 
import os
import sys
import json,time
import re


class Register(QtGui.QDialog):
    def __init__(self):
        super(Register, self).__init__()
        #qss_file = open('white.qss').read()
        #self.setStyleSheet(qss_file)
        self.setWindowTitle(u"注册页面")
       
        label_user = QtGui.QLabel(u"账号",self)
        label_user.setGeometry(QtCore.QRect(75, 55, 50, 22))
        
        label_passwd = QtGui.QLabel(u"密码",self)
        label_passwd.setGeometry(QtCore.QRect(75, 90, 50, 22))
        self.lineEdit_user = QtGui.QLineEdit(self)
        self.lineEdit_user.setPlaceholderText(u'注册密码')
        self.lineEdit_user.setGeometry(QtCore.QRect(110, 55, 150, 22))
     
        self.lineEdit_passwd = QtGui.QLineEdit(self)
        self.lineEdit_passwd.setPlaceholderText(u'注册账号')
        self.lineEdit_passwd.setGeometry(QtCore.QRect(110, 90, 150, 22))
        self.lineEdit_passwd.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_passwd.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[A-Za-z0-9]+"),self))

        SubmitPushbutton=QtGui.QPushButton(u"提交",self)
        SubmitPushbutton.setGeometry(QtCore.QRect(110, 135, 50, 25))
        ClosePushbutton =QtGui.QPushButton(u"关闭",self)
        ClosePushbutton.setGeometry(QtCore.QRect(190, 135, 50, 25))
        #self.resize(400,300)
        SubmitPushbutton.clicked.connect(self.dataBuild)
        ClosePushbutton.clicked.connect(self.close)
    def dataBuild(self):
        User=str(self.lineEdit_user.text())
        Password=str(self.lineEdit_passwd.text())
        data=[User,Password]
        #print User
        #print Password
        path_json="Register.json"
        list_Json=[]
        if os.path.exists (path_json):
            with open(path_json) as file:
                dict_all = json.loads(file.read())
                list_Json=dict_all
        #print list_Json
        list_Json.append(data)
        with open(path_json,"w") as f:
            json.dump(list_Json,f)
        QtGui.QMessageBox.information(self, u"提示",u"注册成功")
        self.close()
        
        

