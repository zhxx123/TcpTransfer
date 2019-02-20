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
SIZEOF_INT64=8
SIZEOF_HEAD_INT=SIZEOF_INT64*2
FileBlockSize=10*1024*1024
class TcpSocket(QTcpSocket):
    signRecv=QtCore.pyqtSignal(str)#
    signFileRecv=QtCore.pyqtSignal("QByteArray")
    signLog=QtCore.pyqtSignal(str)
    def __init__(self, socketId, parent=None):
        super(TcpSocket, self).__init__(parent)
        self.fileBytes = 0
        self.headSize=0
        self.blockBytes=FileBlockSize
        self.socketId = socketId
        self.readyRead.connect(self.readMessage)
        self.disconnected.connect(self.closeConnect)

    def readMessage(self):
        # print('server read message',self.tcpSocket.bytesAvailable())
        stream = QDataStream(self) #发送数据是以QByteArray数据类型发送过来的，所以接收数据也应该以此接收
        stream.setVersion(QDataStream.Qt_5_4) #发送和接收数据以相同的编码形式传输
        while self.bytesAvailable()>SIZEOF_HEAD_INT:
            if self.headSize==0:
                self.headSize=stream.readInt64()
                fileBytes=stream.readInt64()
            if self.bytesAvailable() >= self.headSize + fileBytes:
                qheader = stream.readQString()
                # print("server recv head:",self.headSize,qheader)
                # if self.bytesReceive >= self.headSize+self.fileBytes+SIZEOF_HEAD_INT:
                qfilecont=stream.readRawData(fileBytes)
                # if self.fileBytes > 0:
                #     qfilecont=""
                # self.bytesReceive += self.fileBytes
                # self.handlerMessage(qheader,qfilecont,self.fileBytes)
                ipaddr=self.peerAddress().toString()+":"+str(self.peerPort());
                self.handlerMessage(qheader,qfilecont,fileBytes)
                # self.signRecv.emit(ipaddr,qheader,qfilecont)
                self.initRecv()
            else:
                break

    def sendMessage(self,qheaer):
        # print("server send",qheaer)
        self.outBlock = QByteArray()
        sendout = QDataStream(self.outBlock, QIODevice.WriteOnly)
        sendout.setVersion(QDataStream.Qt_5_4)
        sendout.writeInt64(0)#占位
        sendout.writeQString(qheaer)
        headBytes = self.outBlock.size()
        sendout.device().seek(0)
        sendout.writeInt64(headBytes-SIZEOF_HEAD_INT)
        # sendout.writeInt64(0)
        self.write(self.outBlock)#head
    def handlerMessage(self,qheader,qfilecont,fileBytes):
        headStr=json.loads(qheader)
        type=0
        if "type" in headStr.keys():
            type=headStr["type"]
        
        if  type == 0:#default
            pass
        elif type == 1:# message
            if "msg" in headStr.keys():
                msg=headStr["msg"]
                self.signRecv.emit(msg)
                # qheaders=self.confirmHeader(3)#recv one block file complate
                # self.sendConfirm(qheaders)
        elif type == 2:#file
            filename,filelen,fnum=self.parseJsonFile(headStr)
            fstart=fnum*self.blockBytes
            # print(filename,filelen,fstart)
            self.writeToFile(filename,fnum,fstart,qfilecont,fileBytes)
            # qheaders=self.confirmHeader(3)#recv one block file complate
            # self.sendConfirm(qheaders)
        elif type ==3:
            log_content="recv file complete"
            self.signLog.emit(log_content)
        else:
            print ("error,header",qheader)
    
    def sendConfirm(self,header):
        self.sendMessage(header)
    def confirmHeader(self,type=3):
        data={}
        data["type"]=type
        data["msg"]="send"
        data["status"] =0
        strs=json.dumps(data)
        return strs
    def writeToFile(self,filename,fnum,fstart,qfilecont,fileBytes):
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
    def parseJsonFile(self,jsonStr):
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
    def initRecv(self):
        self.headSize=0
        # self.bytesReceive=0
        self.fileBytes=0
    def closeConnect(self):
        # print('server closeConnect')
        self.disconnectFromHost()
        self.close()
class ServerSocketThread(QtCore.QThread):
    signRecv=QtCore.pyqtSignal(str)
    signLog=QtCore.pyqtSignal(str)
    signSend=QtCore.pyqtSignal(str,str,int)
    def __init__(self, socketId, parent):
        super(ServerSocketThread, self).__init__(parent)
        self.socketId = socketId
        
    def run(self):
        # print("socket thread run")
        clientSocket = TcpSocket(self.socketId)
        if not clientSocket.setSocketDescriptor(self.socketId):
            return
        # print("ip:",ips,"port:",port)
        # ip = str(clientSocket.peerAddress().toString()) # 获取对方的IP地址
        # port = str(clientSocket.peerPort()) # 获取对方的端口号
        # ips=ip[ip.rfind(":"):]

        # socket ->this thread
        clientSocket.signRecv.connect(self.slotRecvMsg)
        clientSocket.signLog.connect(self.soltLogPrint)
        # this thread - > socket
        self.signSend.connect(self.slotSendMsg)
        self.exec_()
    def slotRecvMsg(self,msg):
        self.signRecv.emit(msg)
        pass
    def slotSendMsg(self,msg):
        pass
    def soltLogPrint(self,logMsg):
        self.signLog.emit(logMsg)
class TcpServer(QTcpServer):
    signRecv = QtCore.pyqtSignal(str)
    signLog = QtCore.pyqtSignal(str)
    # 存放socket id
    socketList = []
    # clientDict={}
    def __init__(self, parent=None):
        super(TcpServer, self).__init__(parent)
 
    def incomingConnection(self,socketId):

        if socketId in self.socketList:
            # print("socket in id")
            return 
        self.socketList.append(socketId)

        #新建线程
        # print("stat to socket thread")
        socket_t=ServerSocketThread(socketId,self)
        socket_t.signRecv.connect(self.soltRecvMsg)
        socket_t.signLog.connect(self.soltLogPrint)
        socket_t.start()
    def soltRecvMsg(self,msg):
        self.signRecv.emit(msg)
    def soltLogPrint(self,logMsg):
        self.signLog.emit(logMsg)
class Server(QtCore.QThread):
    signRecv = QtCore.pyqtSignal(str)
    signLog = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(Server, self).__init__(parent)

        self.tcpServer = TcpServer(self)  #指定父对象自动回收空间 监听套接字                     
        self.tcpServer.listen(QHostAddress.Any, 8888) #通信套接字 any默认绑定当前网卡的所有IP
        self.tcpServer.signRecv.connect(self.soltRecvMsg)
        self.tcpServer.signLog.connect(self.soltRecvLogMsg)
    def soltRecvMsg(self,msg):
        self.signRecv.emit(msg)
    def soltRecvLogMsg(self,logMsg):
        self.signLog.emit(logMsg)