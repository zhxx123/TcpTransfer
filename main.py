# -*- coding: utf-8 -*-
from PyQt5.QtNetwork import (QTcpSocket, QTcpServer,QHostAddress)
from PyQt5.QtCore import (QByteArray, QDataStream, QIODevice)
import socket
import sys
import os
import math
import random
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from gui import Ui_MainWindow
from server import Server
from client import *
import time

def _toUTF8(s):
    return str(s)
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class mywindow(QtWidgets.QMainWindow,Ui_MainWindow):
    signSend = QtCore.pyqtSignal(str,str,str,int,str) #ip,port, type, msg
    def __init__(self,parent=None):  
        super(mywindow,self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("../config/py1.ico"))
        # self.lineEdit_2.setFocusPolicy(False)
        self.lineEdit_2.setEnabled(False)
        self.islogin=False
        self.id="id0"
        self.log_numer = 0
        # log 缓冲区大小
        self.max_log_num = 100
        #socket image
        self.server_ip="127.0.0.1"
        self.server_port="8721"
        #初始化 链接
        # time update #槽函数
        self.timer =QtCore.QTimer(self)
        self.timer.timeout.connect(self.setTime)
        self.setTime()
        self.timer.start(1000)
        # sendline signal
        self.widget_my.fileSignal.connect(self.slotSendLine)
        self.lineEdit_fname_msg.returnPressed.connect(self.slotSendLineMsg)
        #tcp server 
        self.server = Server()
        self.server.signRecv.connect(self.slotRecvMsgFromServer)
        self.server.signLog.connect(self.slotRecvLogServer)
        self.server.start()
        # self.sthread = threading.QThread()
        # self.server.moveToThread(self.sthread)
        # self.sthread.started.connect(self.server.run)

        port=_toUTF8(self.lineEdit_2.text())
        log_content="server listen *:%s" %(port)
        self.logprint(log_content)

        # tcp client
        self.client = Client()
        # MainUi->Client
        self.signSend.connect(self.client.slotSendMsg)
        # Client->MainUi
        self.client.signLog.connect(self.soltLogPrint)
        self.client.signFileBtn.connect(self.soltFileUi)
        self.client.signFileBar.connect(self.soltFileBar)
        self.client.signFileSpeed.connect(self.soltFileSpeed)
        self.client.start()
        # thread_t =threading.Thread(target=self.getScrollText,args=(self.sigSetTime,))
        # thread_t.setDaemon(True)
        # thread_t.start()
        # ***************************************
        # self.t =QtCore.QTimer(self)
        # self.t.timeout.connect(self.changeTxtPosition)
        # self.txt="oihp89qruewqe0fad0s;werjafo"
        # self.changeTxtPosition()
        # self.t.start(2000)

    def setTime(self):
        now_time=self.getTime()
        self.label_time_content.setText(now_time)

    def getTimeAndSetTime(self,setTimeSignal):
        while(True):
            setTimeSignal.emit()
            time.sleep(1)

    #*************** tool function *****************
    def getTime(self):
        # formats="%Y-%m-%d %H:%M:%S"
        formats="%Y-%m-%d %H:%M"
        now_time = time.strftime(formats,time.localtime())
        return now_time

    def ToQUtf8(self,strs):
        return _fromUtf8(strs)
    #***************end tool function *****************

    @QtCore.pyqtSlot()
    def on_pushButton_log_clicked(self):
        if not self.islogin:
            value, ok = QtWidgets.QInputDialog.getText(self, "登录", "请入任意用户名\n", QtWidgets.QLineEdit.Normal, "")
            if ok:
                self.id=value
            else:
                self.id="id"+str(random.randint(1,99))
            username="hello, "+self.id+"!"
            self.label_head_user.setText(username)
            log_content="login successful,use random id: %s" %(self.id)
            self.logprint(log_content)
            #登录函数
            self.login_process = LoginHandler(self.id)
            #登陆完成的信号绑定到登陆结束的槽函数
            self.login_process.finishSignal.connect(self.soltLoginEnd)
            #启动线程
            self.login_process.start()
            self.islogin=True
        else:
            log_content="loginout, %s" %(self.id)
            self.logprint(log_content)
            self.login_init()

        # self.label_scroll.setText(_fromUtf8("测试版!!!"))

        # self.sigSetTime.connect(self.setScrollText)
        # #信号函数,信号参数
        # thread_t =threading.Thread(target=self.getScrollText,args=(self.sigSetTime,))
        # thread_t.setDaemon(True)
        # thread_t.start()

    @QtCore.pyqtSlot()
    def on_pushButton_send_msg_clicked(self):
        self.slotSendLineMsg()

    @QtCore.pyqtSlot()
    def on_pushButton_send_file_clicked(self):
        #获取信息
        self.server_ip=_toUTF8(self.lineEdit.text())
        self.server_port=_toUTF8(self.lineEdit_2.text())
        files=_toUTF8(self.lineEdit_fname.text())
        if files!='':
            if not self.isExistFile(files):
                log_content="'%s' not files or not exists!" %(files)
                self.logprint(log_content)
                return
            #process_bar
            self.widget_my.progressBa_send.show()
            self.widget_my.progressBa_send.setValue(0)

            self.signSend.emit(self.server_ip,self.server_port,self.id,2,files)
            
            log_content="send %s to %s" %(files,self.server_ip)
            self.logprint(log_content)
            self.pushButton_send_file.setEnabled(False)
        # else:
        #     log_content="send file is empty!!!"
        #     self.logprint(log_content)

    @QtCore.pyqtSlot(str,str)
    def slotRecvMsgFromServer(self,ids,msg):
        self.logprintmsg(ids,msg)
        # self.pushButton_send_file.setEnabled(True)
    def slotRecvLogServer(self,logMsg):
        self.logprint(logMsg)

    @QtCore.pyqtSlot(str)
    def soltLoginEnd(self,ipaddr):
        self.lineEdit.setText(ipaddr)
        # self.pushButton_log.setDisabled(True)
        log_content="set default ip: %s" %(ipaddr)
        self.logprint(log_content)
    def login_init(self):
        self.label_head_user.setText("")
        self.islogin=False
    @QtCore.pyqtSlot(str)
    def soltLogPrint(self, logMsg):
        self.logprint(logMsg)
        # log_content="disconnect from %s:%s" %(self.server_ip,self.server_port)
    @QtCore.pyqtSlot(int)
    def soltFileUi(self, flag):
        if flag ==1:
            self.pushButton_send_file.setEnabled(True)

    @QtCore.pyqtSlot(int,int)
    def soltFileBar(self,maxnum,nownum):
        self.widget_my.progressBa_send.setMaximum(maxnum)
        self.widget_my.progressBa_send.setValue(nownum)

    @QtCore.pyqtSlot(str,str)
    def soltFileSpeed(self,str_time,str_speed):
        self.widget_my.label_time_2.setText(str_time)
        self.widget_my.label_speed_2.setText(str_speed)

    @QtCore.pyqtSlot(str)
    def slotSendLine(self, words):
        self.lineEdit_fname.setText(words)
        self.pushButton_send_file.setEnabled(True)
    def slotSendLineMsg(self):
        self.server_ip=_toUTF8(self.lineEdit.text())
        self.server_port=_toUTF8(self.lineEdit_2.text())
        msg=_toUTF8(self.lineEdit_fname_msg.text())
        if msg!="":
            self.signSend.emit(self.server_ip,self.server_port,self.id,1,msg)
            self.logprintmsg(self.id,msg)
            self.lineEdit_fname_msg.clear()
            
    #logprint
    def setTextStyle(self,strs):
        tmps="    "+strs
        return tmps
    def logprint(self,strs):
        self.log_numer=self.log_numer+1
        log_content=self.ToQUtf8("<font color='gray'>[{}] {}</font>".format(self.log_numer,self.getTime()))
        self.textBrowser_log.append(log_content)
        # print(log_content)
        log_print=self.setTextStyle(strs)
        if self.log_numer>=self.max_log_num:
            self.textBrowser_log.clear()
            self.log_numer=0
            log_content=self.ToQUtf8("已清空缓冲区")
        # self.textBrowser_log.insertPlainText(log_content) #不能自动获取焦点
        # print(log_print)
        self.textBrowser_log.append(log_print)
    def logprintmsg(self,ids,strs):
        self.log_numer=self.log_numer+1
        log_content=self.ToQUtf8("<font color='gray'>[{}] {} {}</font>".format(self.log_numer,self.getTime(),ids))
        self.textBrowser_log.append(log_content)
        # print(log_content)
        log_print=self.setTextStyle(strs)
        if self.log_numer>=self.max_log_num:
            self.textBrowser_log.clear()
            self.log_numer=0
            log_content=self.ToQUtf8("已清空缓冲区")
        # self.textBrowser_log.insertPlainText(log_content) #不能自动获取焦点
        # print(log_print)
        self.textBrowser_log.append(log_print)
    def isExistFile(self,files):
        if not os.path.isfile(files):
            return False
        if not os.path.exists(files):
            return False
        return True
#login 继承自qthread, 多线程
class LoginHandler(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(str)
    def __init__(self,ids, parent=None):
        super(LoginHandler, self).__init__(parent)
        self.id=ids
    def run(self):
        time.sleep(1)
        ipaddr=self.getLocalIP()
        self.finishSignal.emit(ipaddr)
        
    def getLocalIP(self):
        # local ip
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        default_ip="127.0.0.1"
        try:
            s.connect(('8.8.8.8', 80))
            my_addr = s.getsockname()[0]
            return my_addr
        except Exception as ret:
            # 若无法连接互联网使用，会调用以下方法
            try:
                my_addr = socket.gethostbyname(socket.gethostname())
                return my_addr
            except Exception as ret_e:
                self.si.emit("无法获取ip，请连接网络！\n")
        finally:
            s.close()
        return default_ip

if __name__=="__main__":  
    app=QtWidgets.QApplication(sys.argv)
    myshow=mywindow()
    myshow.show()
    sys.exit(app.exec_())  