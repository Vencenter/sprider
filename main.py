#-*- coding:utf-8 -*-
import sys
from  PyQt4 import QtGui
from  PyQt4 import QtCore
from moudle import *
import math
import re
import os
import json
import shutil
import threading
import urllib2
import requests
import  time



headers = {

    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36',
}

#reload(sys)
#sys.setdefaultencoding("utf-8")


class Widget(QtGui.QWidget):
    
    def __init__(self, parent=None):
        super(Widget,self).__init__(parent=parent)
        self.InitUI()
    def InitUI(self):
        self.my_text=[]
        self.threads = []
        self.num_data=[]
        self.mynum=''

        self.timer = QtCore.QTimer(self) #初始化一个定时器
        
        self.setWindowTitle(u"爬取腾讯数据应用程式!")
        url="http://www.77tj.org/tencent"
        reptile_address=QtGui.QLabel(u"爬取网址：")
        reptile_address_LineEdit=QtGui.QLineEdit()
        reptile_address_LineEdit.setText(url)

        label=QtGui.QLabel("               ")
        #export_line1=QtGui.QPushButton(u"导出第一列")
        export_line2=QtGui.QPushButton(u"导出第二列")
        export_line3=QtGui.QPushButton(u"导出第三列")
        

        reptile_data=QtGui.QLabel(u"爬取的信息：")
        self.reptile_data_TextEdit=QtGui.QTextEdit()
        self.reptile_data_TextEdit1=QtGui.QTextEdit()
        self.line1_TextEdit=QtGui.QTextEdit()
        self.line2_TextEdit=QtGui.QTextEdit()

        self.reptile_data_button=QtGui.QPushButton(u"显示爬取信息")
        pailie_data_button=QtGui.QPushButton(u"显示人数信息")
        save_data_button=QtGui.QPushButton(u"储存爬去信息")
        refresh_data_button=QtGui.QPushButton(u"更新爬取信息")
        
        lay1=QtGui.QHBoxLayout()
        lay1.addWidget(reptile_address)
        lay1.addWidget(reptile_address_LineEdit,3)
        lay1.addWidget(label)
        lay1.addWidget(label)
        #lay1.addWidget(export_line1,1)
        lay1.addStretch(1)
        lay1.addWidget(export_line2,1)
        lay1.addWidget(export_line3,1)

        lay2=QtGui.QHBoxLayout()
        lay2.addWidget(reptile_data)

        lay3=QtGui.QHBoxLayout()
        lay3.addWidget(self.reptile_data_TextEdit1,10)
        lay3.addWidget(self.reptile_data_TextEdit,12)
        lay3.addWidget(self.line1_TextEdit,4)
        lay3.addWidget(self.line2_TextEdit,4)
        

        lay4=QtGui.QHBoxLayout()
        lay4.addWidget(self.reptile_data_button)
        lay4.addWidget(pailie_data_button)
        lay4.addWidget(save_data_button)
        lay4.addWidget(refresh_data_button)


        Layout=QtGui.QVBoxLayout()
        
        Layout.addLayout(lay1)
        Layout.addLayout(lay2)
        Layout.addLayout(lay3)
        Layout.addLayout(lay4)
 
        self.setLayout(Layout)

        self.reptile_data_button.clicked.connect(self.get_data)
        pailie_data_button.clicked.connect(self.slot_data)
        save_data_button.clicked.connect(self.save_data)
        refresh_data_button.clicked.connect(self.refresh_data)
        #export_line1.clicked.connect(self.export_data_line1)
        export_line2.clicked.connect(self.export_data_line2)
        export_line3.clicked.connect(self.export_data_line3)
        self.connect(self.timer,QtCore.SIGNAL("timeout()"),self.refresh_data)
        self.timer.start(60000) #设置计时
       
        
        self.setGeometry(150,30,1200,700)
        
        
        self.show()
       

    def export_data_line1(self):
        filename=QtGui.QFileDialog.getSaveFileName(self,                                             
                  u"文件保存",
                  "./",
                  "Text Files (*.txt);;All Files (*)")

        num_data_list1=self.num_list1
       
        if filename!="":
            f=open(filename,'w')
            if len(num_data_list1)<=1000:
                for i in range(len(num_data_list1)):
                    num1=num_data_list1[i]
                    num_all=str(num1).zfill(3)
                    f.write(num_all+'\n')
            else:
                for i in range(1000):
                    num1=num_data_list1[i]
                    num_all=str(num1).zfill(3)
                    f.write(num_all+'\n')
            f.close()
    def export_data_line2(self):
        filename=QtGui.QFileDialog.getSaveFileName(self,
                                                   
                  u"文件保存",
                  "./",
                  "Text Files (*.txt);;All Files (*)")

        num_data_list2=self.num_list2
        
        if filename!="":
            f=open(filename,'w')
            if len(num_data_list2)<=1000:
                for i in range(len(num_data_list2)):
                    num2=num_data_list2[i]
                    num_all=str(num2).zfill(3)
                    f.write(num_all+'\n')
            else:
                for i in range(1000):
                    num2=num_data_list2[i]
                    num_all=str(num2).zfill(3)
                    f.write(num_all+'\n')
            f.close()
    def export_data_line3(self):
        filename=QtGui.QFileDialog.getSaveFileName(self,                                             
                  u"文件保存",
                  "./",
                  "Text Files (*.txt);;All Files (*)")

        num_data_list3=self.num_list3
        
        
        if filename!="":
            f=open(filename,'w')
            if len(num_data_list3)<=1000:
                for i in range(len(num_data_list3)):
                    num3=num_data_list3[i]
                    num_all=str(num3).zfill(3)
                    f.write(num_all+'\n')
            else:
                for i in range(1000):
                    num3=num_data_list3[i]
                    num_all=str(num3).zfill(3)
                    f.write(num_all+'\n')
            f.close()
    def surf_net(self,index,url):
        try:
            print str(index)
            payload = {'PageIndex': str(index)}
            con = requests.post(url, data=(payload),headers=headers,timeout=2)
            self.my_text.append(con.text)
        except Exception as e:
            try:
                #time.sleep(0.05)
                payload = {'PageIndex': str(index)}
                con = requests.post(url, data=(payload),headers=headers,timeout=2)
                self.my_text.append(con.text)
                print index
            except Exception as e:
                print e
    def save_data(self):
        filename=QtGui.QFileDialog.getSaveFileName(self,                                             
                  u"文件保存",
                  "./",
                  "Text Files (*.txt);;All Files (*)")

        num_data_list1=list(set(self.num_data[0]))
        num_data_list2=list(set(self.num_data[1]))
        num_data_list3=list(set(self.num_data[2]))
        
        if filename!="":
            f=open(filename,'w')
            for i in range(len(self.num_data[2])):
                try:
                    num1=num_data_list1[i]
                    num2=num_data_list2[i]
                    num3=num_data_list3[i]
                except Exception:
                    num1="   "
                    if len(num_data_list3)>len(num_data_list2):
                        try:
                            num2=num_data_list2[i]
                            num3=num_data_list3[i]
                        except Exception:
                            num2="   "
                            try:
                                num3=num_data_list3[i]
                            except Exception:
                                num3="   "
                    else:
                        try:
                            num2=num_data_list2[i]
                            num3=num_data_list3[i]
                        except Exception:
                            num3="   "
                            try:
                                num2=num_data_list2[i]
                            except Exception:
                                num2="   "
                        
                num_all=num1 + "  |  " +num2+"  |  "+num3
                f.write(num_all+'\n')
            f.close()
                
    def refresh_data(self):
        
        new_list=[]
        now_list=[]
        self.num_data=[]
        self.num_data=[]
        url="http://www.77tj.org/tencent"
        
        con = requests.post(url)
        now_list=re.findall(r'<td[^>]*>(.*?)</td>',con.text, re.I | re.M)
        use_list=now_list+self.history_list
        
        for i in range(len(use_list)/3):
            temp=[]
            temp.append(use_list[i*3])
            temp.append(use_list[i*3+1])
            temp.append(use_list[i*3+2].replace("&#x2B;","+"))
            
            new_list.append((temp))


        ids = new_list
        news_ids = []
        for id in ids:
            if id not in news_ids:
                 news_ids.append(id)

        new_list=news_ids

        data=''
        list1=[]
        list2=[]
        list3=[]
        if len(new_list)>=1000:
            for i in range(1000):
                print str(i+1)+"/1000"
                list1.append(new_list[i][1].split(",")[0])
            
                list2.append(new_list[i][1].split(",")[1])
                list3.append(new_list[i][1].split(",")[2])
                date=new_list[i][0]
                num=new_list[i][1]
                flost=new_list[i][2]
                data_url="id:" + str(i+1).zfill(3) +"      date:"+date+"       num:" + num + "\n"
            
                data=data+data_url

        else:
            for i in range(len(new_list)):
                print str(i+1)+"/"+str(len(new_list))
                list1.append(new_list[i][1].split(",")[0])
            
                list2.append(new_list[i][1].split(",")[1])
                list3.append(new_list[i][1].split(",")[2])
                date=new_list[i][0]
                num=new_list[i][1]
                flost=new_list[i][2]
                data_url="id:" + str(i+1).zfill(3) +"       date:"+date+"       num:"+num+"\n"
                data=data+data_url

 
        self.num_data.append(list1)
        self.num_data.append(list2)
        self.num_data.append(list3)
       

        self.history_list=use_list
        self.reptile_data_TextEdit1.setText(data)
        self.slot_data()
        #QtGui.QMessageBox.information(self,"Information",(u"更新完成!"))
      
        
    def slot_data(self):
        self.reptile_data_TextEdit.setText("")
        data=''
        num1_lt=[]
        num2_lt=[]
        num3_lt=[]
        for i in range(len(self.num_data[0])):
            num1=self.num_data[0][i]
            num2=self.num_data[1][i]
            num3=self.num_data[2][i]
            num1_lt.append(int(num1))
            num2_lt.append(int(num2))
            num3_lt.append(int(num3))
            num=num1+"\t  "+num2+"\t  "+num3+"\n"
            data=data+num
        
        num1_set=set(num1_lt)
        num1_set=sorted(num1_set,reverse=True)
        num1_set_count=[]
        for i in num1_set:
            num1_set_count.append(num1_lt.count(i))
            #print('%d 出现了 %d 次!'%(i,num1_lt.count(i)))

        num2_set=set(num2_lt)
        num2_set=sorted(num2_set,reverse=True)
        num2_set_count=[]
        for i in num2_set:
            num2_set_count.append(num2_lt.count(i))
            #print('%d 出现了 %d 次!'%(i,num2_lt.count(i)))
            

        num3_set=set(num3_lt)
        num3_set=sorted(num3_set,reverse=True)
        num3_set_count=[]
        for i in num3_set:
            num3_set_count.append(num3_lt.count(i))
            #print('%d 出现了 %d 次!'%(i,num3_lt.count(i)))
        self.mynum=''
        num1_set=list(num1_set)
        num2_set=list(num2_set)
        num3_set=list(num3_set)
        num1_set_count,num1_set=zip(*sorted(zip(num1_set_count,num1_set),reverse=True))
        num2_set_count,num2_set=zip(*sorted(zip(num2_set_count,num2_set),reverse=True))
        num3_set_count,num3_set=zip(*sorted(zip(num3_set_count,num3_set),reverse=True))

        self.num_list1=num1_set
        self.num_list2=num2_set
        self.num_list3=num3_set
    
        if len(num1_set)>=1000:
            for i in range(1000):
                try:
                    one=str(num1_set[i]).zfill(3)+ "  " +str(num1_set_count[i])
                    two=str(num2_set[i]).zfill(3)+ "  " +str(num2_set_count[i])
                    three=str(num3_set[i]).zfill(3)+ "  " +str(num3_set_count[i])
                    
                except Exception as e:
                    one ="       "
                    try:
                        two=str(num2_set[i]).zfill(3)+ "  " +str(num2_set_count[i])
                        three=str(num3_set[i]).zfill(3)+ "  " +str(num3_set_count[i])
                    except Exception as e:
                        two ="       "
                        try:
                            three=str(num3_set[i]).zfill(3)+ "  " +str(num3_set_count[i])
                        except Exception as e:
                            three ="    "

                pro="   \t \t " +two+"\t \t "+three+"\n"
            
                self.mynum=self.mynum+pro
        else:
            if len(num3_set)>len(num2_set):
                for i in range(len(num3_set)):
                    try:
                        one=str(num1_set[i]).zfill(3)+ ":" +str(num1_set_count[i]).zfill(3)
                        two=str(num2_set[i]).zfill(3)+ ":" +str(num2_set_count[i]).zfill(3)
                        three=str(num3_set[i]).zfill(3)+ ":" +str(num3_set_count[i]).zfill(3)
                        
                    except Exception as e:
                        one ="       "
                        try:
                            two=str(num2_set[i]).zfill(3)+ ":" +str(num2_set_count[i]).zfill(3)
                            three=str(num3_set[i]).zfill(3)+ ":" +str(num3_set_count[i]).zfill(3)
                        except Exception as e:
                            
                            two ="       "
                            
                            try:
                                three=str(num3_set[i]).zfill(3)+ ":" +str(num3_set_count[i]).zfill(3)
                            except Exception as e:
                                three ="    "

                    pro="   \t  " +two+"\t \t "+three+"\n"
                    
                    

                    self.mynum=self.mynum+pro
            else:
                for i in range(len(num2_set)):
                    try:
                        one=str(num1_set[i]).zfill(3)+ ":" +str(num1_set_count[i]).zfill(3)
                        two=str(num2_set[i]).zfill(3)+ ":" +str(num2_set_count[i]).zfill(3)
                        three=str(num3_set[i]).zfill(3)+ ":" +str(num3_set_count[i]).zfill(3)
                        
                    except Exception as e:
                        one ="       "
                        try:
                            two=str(num2_set[i]).zfill(3)+ ":" +str(num2_set_count[i]).zfill(3)
                            three=str(num3_set[i]).zfill(3)+ ":" +str(num3_set_count[i]).zfill(3)
                        except Exception as e:
                            
                            three ="       "
                            
                            try:
                                two=str(num2_set[i]).zfill(3)+ ":" +str(num2_set_count[i]).zfill(3)
                            except Exception as e:
                                two ="    "

                    pro="   \t  " +two+"\t \t   "+three+"\n"
                    
                    

                    self.mynum=self.mynum+pro

        self.reptile_data_TextEdit.setText(self.mynum)
        my_two_data=''
        if len(num2_set)>=1000:
            for i in range(1000):
                two1=str(num2_set[i]).zfill(3)+ ":" +str(num2_set_count[i]).zfill(3)
                my_two_data=my_two_data+two1+"\n"
        else:
            for i in range(len(num2_set)):
                two1=str(num2_set[i]).zfill(3)+ ":" +str(num2_set_count[i]).zfill(3)
                my_two_data=my_two_data+two1+"\n"
        my_three_data=''
        if len(num3_set)>=1000:
            for i in range(1000):
                three1=str(num3_set[i]).zfill(3)+ ":" +str(num3_set_count[i]).zfill(3)
                my_three_data=my_three_data+three1+"\n"
        else:
            for i in range(len(num3_set)):
                three1=str(num3_set[i]).zfill(3)+ ":" +str(num3_set_count[i]).zfill(3)
                my_three_data=my_three_data+three1+"\n"
        
        self.line1_TextEdit.setText(my_two_data)
        self.line2_TextEdit.setText(my_three_data)
        
                
            
            
        #self.reptile_data_TextEdit.setText(data)
        
        
    def get_data(self):
        self.reptile_data_button.setEnabled(0)
        self.my_text=[]
        self.threads = []
        self.num_data=[]
        url="http://www.77tj.org/tencent"
        
        for index in range(1,35):
            
            try:
                one_thread = threading.Thread(target=self.surf_net(index,url), args=(index,url,))
                
                self.threads.append(one_thread)
            except Exception as e:
               print e

        for j in self.threads:
            j.start()

        for j in self.threads:
            j.join()
            
        self.my_text=str(self.my_text)
        self.lt=re.findall(r'<td[^>]*>(.*?)</td>',self.my_text, re.I | re.M)
        
        self.data=''
        list1=[]
        list2=[]
        list3=[]
        
        for i in range(0,len(self.lt)/3):
            try:
                print str(i+1)+"/"+str(len(self.lt)/3)
                n=str(i+1)
                s = n.zfill(3)
                self.lt[i*3+2]=self.lt[i*3+2].replace("&#x2B;","+")
                num=self.lt[i*3+1].split(",")
                list1.append(num[0])
                list2.append(num[1])
                list3.append(num[2])
                data_url="id:" + s +"       date:"+self.lt[i*3]+"       num:"+self.lt[i*3+1]+"\n"
                self.data=self.data+data_url            
            except Exception as e:
                print(u"出现异常-->!")
                
                                             
        self.num_data.append(list1)
        self.num_data.append(list2)
        self.num_data.append(list3)
        
        self.history_list=self.lt
        
                                             
        self.reptile_data_TextEdit1.setText(self.data)
        QtGui.QMessageBox.information(self,"Information",(u"爬取完成!"))
        


if __name__ == '__main__': 
    app = QtGui.QApplication(sys.argv)
    dialog = login()   
    if dialog.exec_():
        win=Widget()
        win.show()
        sys.exit(app.exec_())
        #sys.exit()     
    

