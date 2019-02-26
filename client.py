# -*- coding: utf-8 -*-
from PyQt5.QtNetwork import (QTcpSocket, QTcpServer,QHostAddress)
from PyQt5.QtCore import (QByteArray, QDataStream, QIODevice)
from socket import *
import sys
import os
import math
import json
import random
from PyQt5 import QtCore, QtGui, QtWidgets
from gui import Ui_MainWindow
import time
import threading
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

class TcpClient(QtCore.QThread):
    socketlist=[]
    socketInfo={}
    signRecv=QtCore.pyqtSignal(str)
    signLog=QtCore.pyqtSignal(str)
    signFileBtn=QtCore.pyqtSignal(int)
    signFileBar=QtCore.pyqtSignal(int,int)
    signThread=QtCore.pyqtSignal(str,int,int,"QByteArray")
    signConfirm=QtCore.pyqtSignal(str)
    signFileSpeed=QtCore.pyqtSignal(str,str)
    def __init__(self,parent=None):
        super(TcpClient, self).__init__(parent)
        self.blockBytes=FileBlockSize
        # self.bytesReceive=0
        self.fileBytes = 0
        self.headSize=0
        self.flag=False
        # self.sendInit()
        self.signThread.connect(self.sendFile)
        self.signConfirm.connect(self.sendFileConfirm)
    def isconnect(self,ip):
        if ip in self.socketlist:
            return True
        return False

    def setIpPort(self,ip,port,ids,msgtype,msg):
        self.server_ip=ip
        self.server_port=port
        self.filename=msg
        self.msgtype=msgtype
        self.id=ids
    def slotTcpSendMsg(self,ips,ports,ids,types,msgs):
        # print("tcpclient send msg:",ips,ports,types,msgs)
        self.setIpPort(ips,ports,ids,types,msgs)
        if not self.isconnect(ips):
            self.tcpSocket=QTcpSocket()
            self.tcpSocket.connected.connect(self.connected)
            self.tcpSocket.readyRead.connect(self.readMessage)
            self.tcpSocket.error.connect(self.connError)
            self.tcpSocket.connectToHost(self.server_ip, int(self.server_port))
            log_content="connect to %s:%s ..." %(self.server_ip,self.server_port)
            self.signLog.emit(log_content)
            if not self.tcpSocket.waitForConnected(500):
                msg = self.tcpSocket.errorString()
                self.signLog.emit(msg)
                self.closeConnect()
                self.signFileBtn.emit(1)
                return
            self.socketlist.append(ips)
            self.socketInfo[ips]=self.tcpSocket
            return
        if ips in self.socketInfo.keys():
            self.tcpSocket=self.socketInfo[ips]
            self.sendMessage()
    def connError(self):
        self.signLog.emit("connect error")
        self.closeConnect()
    def connected(self):
        self.sendMessage()

    def sendLocalMsg(self,filename):
        # self.sendInit()
        qheaer=self.getHeaderMsg(filename);
        self.sendHeaderMsg(qheaer)
        # self.sendInit()
    def sendMessage(self):
        if self.msgtype==1:
            self.sendLocalMsg(self.filename)
        elif self.msgtype == 2:
            # log_content="connected,start to send file"
            # self.signLog.emit(log_content)
            self.sendMsgFile(self.filename)
    def sendMsgFile(self,filename):
        self.flag=True
        crthread = threading.Thread(target=self.readFile, args=(filename,self.blockBytes))
        crthread.daemon = True  # 设置随主线程退出
        crthread.start()
        self.flag=False
        
    def readFile(self,filename,blockbytes):
        # print("send file",filename)
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
        start_time=int(time.time())
        tmp_time=start_time
        tmp_speed=""
        tmp_total_time=""
        while not fstream.atEnd():
            readsize=min(totalFBytes,self.blockBytes)
            totalFBytes-=readsize
            filecont=fstream.readRawData(readsize)
            # print("send",i,readsize)
            self.signThread.emit(fname,i,readsize,filecont)         
            i+=1
            self.signFileBar.emit(fnum,i)
            self.flag=True
            while self.flag:
                if len(tmp_speed)>0:
                    self.signFileSpeed.emit(time_total_time+"s",self.getRandomTime(tmp_speed))
                time.sleep(0.5)
            now_time=int(time.time())
            about_time,speed=self.getAboutTime(now_time-tmp_time+0.1,readsize,totalFBytes)
            self.signFileSpeed.emit(about_time+"s",speed)
            tmp_time=now_time
            tmp_speed=speed
            time_total_time=about_time
        localfile.close()
        self.signFileBar.emit(fnum,fnum)
        now_time=int(time.time())
        ab_time=self.getTimeFromat(now_time-start_time)+"s"
        self.signFileSpeed.emit(ab_time,"")
        self.signConfirm.emit(fname)
    def getRandomTime(self,speed):
        increment=random.randint(-2,3)
        increment_dot=random.randint(-5,8)
        speeds=""
        if 'MB' in speed:
            speeds=str(float(speed[:-2])+increment*0.1)+"MB"
        elif 'KB' in speed:
             speeds=str(float(speed[:-2])+increment*2+increment_dot*0.05)+"KB"
        elif 'B' in speed:
             speeds=str(float(speed[:-1])+increment)+"B"
        return speeds
    def getAboutTime(self,timespan,readsize,totalsize):
        speed=round(readsize/timespan,2)
        if timespan == 0.1:
            speed/=10
        about_time=int(totalsize/speed)
        sp_unit="B"
        if speed>=1024:
            sp_unit="KB"
            speed=round(speed/1024,2)
        if speed>=1024:
            sp_unit="MB"
            speed=round(speed/1024,2)
        ab_result=self.getTimeFromat(about_time)
        sp_result=str(speed)+sp_unit
        return ab_result,sp_result
    def getTimeFromat(self,about_time):
        ab_unit=[]
        if about_time>=60:
            ab_unit.append(str(about_time%60))
            about_time=int(about_time/60)
        if about_time>=60:
            ab_unit.append(str(about_time%60))
            about_time=int(about_time/60)
        ab_unit.append(str(about_time))
        tmp_ab=ab_unit[::-1]
        ab_result=':'.join(tmp_ab)
        return ab_result
    def sendConfirm(self):
        qheaer=self.confirmHeader();
        self.sendHeaderMsg(qheaer)
    def sendFileConfirm(self,fname):
        qheaer=self.confirmHeader(3,fname);
        self.sendHeaderMsg(qheaer)
    def readMessage(self):
        stream = QDataStream(self.tcpSocket)
        stream.setVersion(QDataStream.Qt_5_4)
        while self.tcpSocket.bytesAvailable()>SIZEOF_HEAD_INT:
            if self.headSize==0:
                self.headSize=stream.readInt64()
                # fileBytes=stream.readInt64()
                # self.bytesReceive+=SIZEOF_HEAD_INT
            if self.tcpSocket.bytesAvailable() >= self.headSize:
                qheader = stream.readQString()
                # print("client recv head:",qheader)
                # self.bytesReceive += self.headSize
                self.handlerMessage(qheader)
                self.initRecv()
            else:
                break
    def handlerMessage(self,headers):
        if len(headers)<1:
            return
        headStr=json.loads(headers)
        type=0
        if "type" in headStr:
            type=headStr["type"]
        if type==3:
            if "status" in headStr and  headStr["status"]==0:
                self.flag=False
                # self.closeConnect()#断开连接
    def sendFile(self,fname,fnum,filelen,filecont):
        self.sendInit()
        qheader=self.getHeader(fname,filelen,fnum,2);
        self.sendmsg(qheader,filecont)
        # self.sendInit()
    def sendmsg(self,qheader,filecont):
        self.outBlock = QByteArray()
        sendout = QDataStream(self.outBlock, QIODevice.WriteOnly)
        sendout.setVersion(QDataStream.Qt_5_4)
        sendout.writeInt64(0)#占位
        sendout.writeInt64(0)
        
        sendout.writeQString(qheader)
        headBytes = self.outBlock.size()

        sendout.writeRawData(filecont)
        fileBytes=self.outBlock.size()-headBytes
    
        sendout.device().seek(0)
        sendout.writeInt64(headBytes-SIZEOF_HEAD_INT)
        sendout.writeInt64(fileBytes)
        self.tcpSocket.write(self.outBlock)#head

    def sendHeaderMsg(self,qheader):
        self.outBlock = QByteArray()
        sendout = QDataStream(self.outBlock, QIODevice.WriteOnly)
        sendout.setVersion(QDataStream.Qt_5_4)
        sendout.writeInt64(0)#占位
        sendout.writeInt64(0)
        
        sendout.writeQString(qheader)
        headBytes = self.outBlock.size()
    
        sendout.device().seek(0)
        sendout.writeInt64(headBytes-SIZEOF_HEAD_INT)
        self.tcpSocket.write(self.outBlock)#head

    def closeConnect(self):
        log_content="client disconnect to %s" %(self.server_ip)
        self.signLog.emit(log_content)
        self.tcpSocket.disconnectFromHost()
        self.tcpSocket.close()
        # self.sign.emit(1)
    def initRecv(self):
        self.headSize=0
    def sendInit(self):
        # print("client sent init")
        self.fileBytes=0
        # self.flag=False
    def getHeader(self,fname,flen,fnum,type=0):
        data={}
        data["type"]=type
        data["id"] =self.id
        data["filename"]=fname
        data["filelen"]=flen
        data["fnum"]=fnum
        strs=json.dumps(data)
        return _fromUtf8(strs)
    def confirmHeader(self,type=3,fname=""):
        data={}
        data["type"]=type
        data["id"] =self.id
        data["confirm"]="send"
        data["status"] =0
        if fname != "":
            data["filename"]=fname
        strs=json.dumps(data)
        return _fromUtf8(strs)
    def getHeaderMsg(self,contant):
        data={}
        data["type"]=1
        data["msg"]=contant
        data["id"] =self.id
        strs=json.dumps(data)
        return _fromUtf8(strs)

class Client(QtCore.QThread):
    signRecv=QtCore.pyqtSignal(str)
    signLog=QtCore.pyqtSignal(str)
    signFileBtn=QtCore.pyqtSignal(int)
    signFileBar=QtCore.pyqtSignal(int,int)
    signSend=QtCore.pyqtSignal(str,str,str,int,str) #ip,port, type, msg
    signFileSpeed=QtCore.pyqtSignal(str,str)
    def __init__(self,parent=None):
        super(Client, self).__init__(parent)
        self.id="zhxx"
        self.ip="127.0.0.1"
        self.port="8721"
    def run(self):
        tcpclient=TcpClient()
        # client -> tcpclient
        self.signSend.connect(tcpclient.slotTcpSendMsg)
        # client -> MainUi
        # self.signLog.connect()
        # tcpclient -> client
        tcpclient.signRecv.connect(self.soltRecvMsg)
        tcpclient.signFileBtn.connect(self.soltFileUi)
        tcpclient.signFileBar.connect(self.soltFileBar)
        tcpclient.signLog.connect(self.soltLogPrint)
        tcpclient.signFileSpeed.connect(self.soltFileSpeed)
        tcpclient.start()
        self.exec_()
        # print("client init")
    def soltRecvMsg(self,msg):
        # print(msg)
        pass
    def slotSendMsg(self,ips,ports,ids,types,msg):
        # print("client send msg",ips,ports,types,msg)
        self.signSend.emit(ips,ports,ids,types,msg)
        pass
    def soltFileUi(self,flag):
        self.signFileBtn.emit(flag)
        pass
    def soltFileBar(self,total,now):
        self.signFileBar.emit(total,now)
    def soltFileSpeed(self,str_time,str_speed):
        self.signFileSpeed.emit(str_time,str_speed)
        pass
    def soltLogPrint(self,logMsg):
        self.signLog.emit(logMsg)
        # print(content)