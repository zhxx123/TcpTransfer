# -*- coding: utf-8 -*-
from PyQt5.QtNetwork import (QTcpSocket, QTcpServer,QHostAddress)
from PyQt5.QtCore import (QByteArray, QDataStream, QIODevice)
from socket import *
import sys
import os
import math
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from gui import Ui_MainWindow
import time

def _toUTF8(s):
    return str(s)
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class mywindow(QtWidgets.QMainWindow,Ui_MainWindow):
    # sigSetTime = QtCore.pyqtSignal(str) 
    def __init__(self,parent=None):  
        super(mywindow,self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("../config/py1.ico"))
        # self.lineEdit_2.setFocusPolicy(False)
        self.lineEdit_2.setEnabled(False)
        self.log_numer = 0
        # log 缓冲区大小
        self.max_log_num = 100
        #socket image
        self.server_ip="127.0.0.1"
        self.server_port="8888"
        #初始化 链接
        # time update #槽函数
        self.timer =QtCore.QTimer(self)
        self.timer.timeout.connect(self.setTime)
        self.setTime()
        self.timer.start(1000)
        # sendline signal
        self.widget_my.fileSignal.connect(self.SetSendLine)

        #tcp server 
        self.server_process = TcpServer()
        self.server_process.serverSignal.connect(self.ServerSloat)
        self.server_process.start()
        port=_toUTF8(self.lineEdit_2.text())
        log_content="server listen *:%s" %(port)
        self.logprint(log_content)
        # tcp client
        #监听 server
        self.client_process = TcpClient()
        self.client_process.clientSignal.connect(self.clientSloat)
        self.client_process.clientUiSignal.connect(self.clientUiSloat)
        self.client_process.clientBarSignal.connect(self.clientBarUpdate)
        self.client_process.start()
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
        formats="%Y-%m-%d %H:%M:%S"
        now_time = time.strftime(formats,time.localtime())
        return now_time

    def ToQUtf8(self,strs):
        return _fromUtf8(strs)
    #***************end tool function *****************

    @QtCore.pyqtSlot()
    def on_pushButton_log_clicked(self):
        #登录函数
        self.login_process = LoginHandler()
        #登陆完成的信号绑定到登陆结束的槽函数
        self.login_process.finishSignal.connect(self.LoginEnd)
        #启动线程
        self.login_process.start()

        self.label_scroll.setText(_fromUtf8("测试版!!!"))
        # self.sigSetTime.connect(self.setScrollText)
        # #信号函数,信号参数
        # thread_t =threading.Thread(target=self.getScrollText,args=(self.sigSetTime,))
        # thread_t.setDaemon(True)
        # thread_t.start()

    @QtCore.pyqtSlot(str)
    def ServerSloat(self, words):
        self.logprint(words)
        # self.pushButton_send_file.setEnabled(True)


    @QtCore.pyqtSlot(str)
    def LoginEnd(self, words):
        self.label_head_user.setText(words)
        self.pushButton_log.setDisabled(False)
        log_content="login succeed, %s" %(words)
        self.logprint(log_content)
    @QtCore.pyqtSlot()
    def on_pushButton_send_msg_clicked(self):
        self.server_ip=_toUTF8(self.lineEdit.text())
        self.server_port=_toUTF8(self.lineEdit_2.text())
        msg=_toUTF8(self.lineEdit_fname_msg.text())
        if msg!="":
            self.client_process.setIpPort(self.server_ip,self.server_port,msg,1)
            msg=self.client_process.toSendMsg()
            if msg != None:
                log_content="error,%s" %(msg)
                self.logprint(log_content)
                return
        else:
            log_content="send msg not empty!!!"
            self.logprint(log_content)
    @QtCore.pyqtSlot()
    def on_pushButton_send_file_clicked(self):
        #获取信息
        self.server_ip=_toUTF8(self.lineEdit.text())
        self.server_port=_toUTF8(self.lineEdit_2.text())
        files=_toUTF8(self.lineEdit_fname.text())
        if files!='':
            if not self.isExistFile(files):
                log_content="%s not files or not exists!" %(files)
                self.logprint(log_content)
                return
            #process_bar
            self.widget_my.progressBa_send.show()
            self.widget_my.progressBa_send.setValue(0)

            self.client_process.setIpPort(self.server_ip,self.server_port,files,0)
            msg=self.client_process.toSendFile()
            if msg != None:
                log_content="error,%s" %(msg)
                self.logprint(log_content)
                return
            
            log_content="start send %s to %s:%s" %(files,self.server_ip,self.server_port)
            self.logprint(log_content)
            self.pushButton_send_file.setEnabled(False)
        else:
            log_content="send file is empty!!!"
            self.logprint(log_content)

    @QtCore.pyqtSlot(str)
    def clientSloat(self, words):
        # print("clientSlot")
        self.logprint(words)
        # log_content="disconnect from %s:%s" %(self.server_ip,self.server_port)
    @QtCore.pyqtSlot(int)
    def clientUiSloat(self, words):
        if words ==1:
            self.pushButton_send_file.setEnabled(True)
    @QtCore.pyqtSlot(int,int)
    def clientBarUpdate(self, maxnum,nownum):
        self.widget_my.progressBa_send.setMaximum(maxnum)
        self.widget_my.progressBa_send.setValue(nownum)
    
    @QtCore.pyqtSlot(str)
    def SetSendLine(self, words):
        self.lineEdit_fname.setText(words)
        self.pushButton_send_file.setEnabled(True)
    
    #logprint
    def logprint(self,strs):
        self.log_numer=self.log_numer+1
        log_content=self.ToQUtf8("[{}] {}\n    {}".format(self.log_numer,self.getTime(),strs))
        if self.log_numer>=self.max_log_num:
            self.textBrowser_log.clear()
            self.log_numer=0
            log_content=self.ToQUtf8("已清空缓冲区")
        # self.textBrowser_log.insertPlainText(log_content) #不能自动获取焦点
        self.textBrowser_log.append(log_content)
    def isExistFile(self,files):
        if not os.path.isfile(files):
            return False
        if not os.path.exists(files):
            return False
        return True
#login 继承自qthread, 多线程
class LoginHandler(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(str)
    def __init__(self,  parent=None):
        super(LoginHandler, self).__init__(parent)

    def run(self):
        time.sleep(1)
        self.finishSignal.emit("hello,zhxx!")

SIZEOF_INT64=8
SIZEOF_HEAD_INT=SIZEOF_INT64*2
FileBlockSize=10*1024*1024
class TcpClient(QtCore.QThread):
    clientSignal = QtCore.pyqtSignal(str)
    clientUiSignal = QtCore.pyqtSignal(int)
    clientBarSignal = QtCore.pyqtSignal(int,int)
    def __init__(self,parent=None):
        super(TcpClient, self).__init__(parent)
        self.tcpSocket = QTcpSocket(self)
        self.tcpSocket.connected.connect(self.connected)
        self.tcpSocket.readyRead.connect(self.readMessage)
        self.tcpSocket.error.connect(self.connError)
        self.msgtype=0;
        self.id="zhxx"
        self.blockBytes=FileBlockSize
        self.bytesReceive=0
        self.fileBytes = 0
        self.headSize=0
        self.sendInit()
    def setIpPort(self,ip,port,filename,msgtype=0):
        self.server_ip=ip
        self.server_port=port
        self.filename=filename
        self.msgtype=msgtype
    def toSendFile(self):
        log_content="connect to %s:%s ..." %(self.server_ip,self.server_port)
        self.clientSignal.emit(log_content)
        self.tcpSocket.connectToHost(self.server_ip, int(self.server_port))
 
        if not self.tcpSocket.waitForConnected(1500):
            msg = self.tcpSocket.errorString()
            self.closeConnect()
            return msg
        return None
    def toSendMsg(self):
        self.tcpSocket.connectToHost(self.server_ip, int(self.server_port))
        if not self.tcpSocket.waitForConnected(500):
            msg = self.tcpSocket.errorString()
            # self.closeConnect()
            return msg
        return None
    def connError(self):
        self.clientSignal.emit("connect error")
        self.closeConnect()
    def connected(self):
        if self.msgtype==1:
            self.sendLocalMsg(self.filename)
        else:
            log_content="connected,start to send file"
            self.clientSignal.emit(log_content)
            self.sendMessage(self.filename)

    def sendMessage(self,filename):
        # print("send message",filename)
        info = QtCore.QFileInfo(filename)
        fname=info.fileName()
        localfile = QtCore.QFile(filename)
        localfile.open(QtCore.QFile.ReadOnly)
        totalFBytes=localfile.size()
        filecont = QByteArray()
        # filecont = self.localfile.read(min(totalFBytes,self.blockBytes))
        fstream = QDataStream(localfile)
        fnum=math.ceil(float(totalFBytes)/self.blockBytes)
        # print("total",totalFBytes)
        # print("blockbytes",self.blockBytes)
        # print("fnum",fnum)
        i=0
        while not fstream.atEnd():
            readsize=min(totalFBytes,self.blockBytes)
            totalFBytes-=self.blockBytes
            filecont=fstream.readRawData(readsize)
            # print("send",i,readsize)
            self.sendFile(fname,i,readsize,filecont)         
            i+=1
            self.clientBarSignal.emit(fnum,i)
        localfile.close()
        self.clientBarSignal.emit(fnum,fnum)
        self.sendConfirm()
    def sendLocalMsg(self,filename):
        self.sendInit()
        qheaer=self.getHeaderMsg(filename);
        self.sendmsg(qheaer)
        self.sendInit()
        self.sendConfirm()

    def sendConfirm(self):
        # print("send confirm")
        self.sendInit()
        qheaer=self.confirmHeader();
        self.sendmsg(qheaer)
        self.sendInit()
    
    def readMessage(self):
        stream = QDataStream(self.tcpSocket)                     #发送数据是以QByteArray数据类型发送过来的，所以接收数据也应该以此接收
        stream.setVersion(QDataStream.Qt_5_4)
        while self.tcpSocket.bytesAvailable()>SIZEOF_HEAD_INT:
            if self.bytesReceive==0 or self.fileBytes ==0 or self.headSize==0:
                self.fileBytes=stream.readInt64()
                self.headSize=stream.readInt64()
                self.bytesReceive+=SIZEOF_HEAD_INT
            if self.tcpSocket.bytesAvailable() >= self.headSize+self.fileBytes:
                qheader = stream.readQString()
                # print("client recv head:",qheader)
                self.bytesReceive += self.headSize
                self.handlerMessage(qheader)
            else:
                break
    def handlerMessage(self,headers):
        headStr=json.loads(headers)
        type=0
        if "type" in headers:
            type=headStr["type"]
        if type==3:
            if "status" in headers and  headStr["status"]==0:
                self.closeConnect()#断开连接
    def sendFile(self,fname,fnum,filelen,filecont):
        self.sendInit()
        qheaer=self.getHeader(fname,filelen,fnum,2);
        self.sendmsg(qheaer,filecont)
        self.sendInit()

    def sendmsg(self,qheaer,filecont=""):
        self.outBlock = QByteArray()
        sendout = QDataStream(self.outBlock, QIODevice.WriteOnly)
        sendout.setVersion(QDataStream.Qt_5_4)
        sendout.writeInt64(0)#占位
        sendout.writeInt64(0)
        
        sendout.writeQString(qheaer)
        if len(filecont)>0:
            headBytes = self.outBlock.size()

            sendout.writeRawData(filecont)
            fileBytes=self.outBlock.size()-headBytes
        
            sendout.device().seek(0)
            sendout.writeInt64(fileBytes)
            sendout.writeInt64(headBytes-SIZEOF_HEAD_INT)
        self.tcpSocket.write(self.outBlock)#head

    def closeConnect(self):
        log_content="client disconnect to %s" %(self.server_ip)
        self.clientSignal.emit(log_content)
        self.tcpSocket.disconnectFromHost()
        self.tcpSocket.close()
        self.clientUiSignal.emit(1)
    def sendInit(self):
        # print("client sent init")
        self.fileBytes=0
        self.headBytes=0
    def getHeader(self,fname,flen,fnum,type=0):
        data={}
        data["type"]=type
        data["filename"]=fname
        data["filelen"]=flen
        data["fnum"]=fnum
        strs=json.dumps(data)
        return _fromUtf8(strs)
    def confirmHeader(self,type=3):
        data={}
        data["type"]=type
        data["confirm"]="send"
        data["status"] =0
        strs=json.dumps(data)
        return _fromUtf8(strs)
    def getHeaderMsg(self,contant):
        data={}
        data["type"]=1
        data["msg"]=contant
        data["id"] =self.id
        strs=json.dumps(data)
        return _fromUtf8(strs)
class TcpServer(QtCore.QThread):
    serverSignal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(TcpServer, self).__init__(parent)
        # self.serverSignal.emit("hello,zhxx!")
        self.tcpServer = QTcpServer()                             #指定父对象自动回收空间 监听套接字
        self.tcpSocket = QTcpSocket()                             #通信套接字
        self.bytesReceive=0
        self.fileBytes = 0
        self.headSize=0
        self.blockBytes=FileBlockSize
        self.tcpServer.listen(QHostAddress.Any, 8888)                 #any默认绑定当前网卡的所有IP
        self.tcpServer.newConnection.connect(self.handleNewConnection)
 
    def handleNewConnection(self):
        # print("server handleNewConnection")
        self.tcpSocket = self.tcpServer.nextPendingConnection()       #取出建立好链接的套接字
        #获取对方IP和端口
        ip = str(self.tcpSocket.peerAddress().toString())                        #获取对方的IP地址
        port = str(self.tcpSocket.peerPort())                              #获取对方的端口号
        ips=ip[ip.rfind(":"):]
        self.serverSignal.emit("server new con %s:%s"%(ips,port))
        self.tcpSocket.readyRead.connect(self.readMessage)
        self.tcpSocket.disconnected.connect(self.closeConnect)
    def sendConfirm(self,header):
        self.sendMessage(header)
    def sendMessage(self,message):
       self.sendmsg(message)
    def sendmsg(self,qheaer):
        self.outBlock = QByteArray()
        sendout = QDataStream(self.outBlock, QIODevice.WriteOnly)
        sendout.setVersion(QDataStream.Qt_5_4)
        sendout.writeInt64(0)#占位
        sendout.writeInt64(0)
        sendout.writeQString(qheaer)
        headBytes = self.outBlock.size()
        sendout.device().seek(0)
        sendout.writeInt64(0)
        sendout.writeInt64(headBytes-SIZEOF_HEAD_INT)
        self.tcpSocket.write(self.outBlock)#head
    def initRecv(self):
        # print("init Recv")
        self.headSize=0
        self.bytesReceive=0
        self.fileBytes=0

    def readMessage(self):
        # print('server read message',self.tcpSocket.bytesAvailable())
        stream = QDataStream(self.tcpSocket)                     #发送数据是以QByteArray数据类型发送过来的，所以接收数据也应该以此接收
        stream.setVersion(QDataStream.Qt_5_4)                  #发送和接收数据以相同的编码形式传输
        while self.tcpSocket.bytesAvailable()>SIZEOF_HEAD_INT:
            if self.bytesReceive==0 or self.fileBytes ==0 or self.headSize==0:
                self.fileBytes=stream.readInt64()
                self.headSize=stream.readInt64()
                self.bytesReceive+=SIZEOF_HEAD_INT
            if self.tcpSocket.bytesAvailable() >= self.headSize+self.fileBytes:
                qheader = stream.readQString()
                self.bytesReceive += self.headSize
                # print("server recv head:",self.headSize,qheader)
                if self.bytesReceive <= self.headSize+self.fileBytes+SIZEOF_HEAD_INT:
                    qfilecont=stream.readRawData(self.fileBytes)
                    self.bytesReceive += self.fileBytes
                    # # print("content:",self.fileBytes,qfilecont)
                    self.handlerMessage(qheader,qfilecont,self.fileBytes)
                self.initRecv()
            else:
                break
    def handlerMessage(self,qheader,qfilecont,fileBytes):
        headStr=json.loads(qheader)
        type=0
        if "type" in headStr.keys():
            type=headStr["type"]
        
        if   type == 0:#default
            pass
        elif type == 1:# message
            if "msg" in headStr.keys():
                msg=headStr["msg"]
                self.serverSignal.emit(msg)
        elif type == 2:#file
            filename,filelen,fnum=parseJsonFile(headStr)
            fstart=fnum*self.blockBytes
            # print(filename,filelen,fstart)
            if fnum==0:
                file = QtCore.QFile(filename)
                if file.exists():
                    file.remove()
            new_file = QtCore.QFile(filename)
            new_file.open(QtCore.QFile.Append)
            fcont = QDataStream(new_file)
            # fcont.device().seek(fstart)
            fcont.writeRawData(qfilecont)
            new_file.close()
        elif type ==3:
            self.sendConfirm(qheader)
            log_content="recv file complete"
            self.serverSignal.emit(log_content)
        else:
            print ("error,header",qheader)
        
    def closeConnect(self):
        # print('server closeConnect')
        self.tcpSocket.disconnectFromHost()
        self.tcpSocket.close()
def parseJsonFile(jsonStr):
    filename=""
    if "filename" in jsonStr.keys():
        filename=jsonStr["filename"]
    filelen=0
    if  "filelen" in jsonStr.keys():
        filelen=jsonStr["filelen"]
    fnum=0
    if  "fnum" in jsonStr.keys():
        fnum=jsonStr["fnum"]
    return filename,filelen,fnum

if __name__=="__main__":  
    app=QtWidgets.QApplication(sys.argv)  
    myshow=mywindow()
    myshow.show()
    sys.exit(app.exec_())  