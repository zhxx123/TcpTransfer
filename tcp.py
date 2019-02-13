# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tcp.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtNetwork import QTcpSocket, QTcpServer, QHostAddress
from PyQt5.QtCore import QByteArray, QDataStream, QIODevice
from PyQt5.QtGui import QPainter
import time
import platform
import sys
import math
import json
from PyQt5 import QtCore, QtGui, QtWidgets
def _toUTF8(s):
    return str(s)
try:
    _fromUtf8 = str
except AttributeError:
    def _fromUtf8(s):
        return s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("传输")
        MainWindow.resize(721, 552)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 50, 721, 471))
        self.tabWidget.setObjectName("tabWidget")
        self.widget = QtWidgets.QWidget()
        self.widget.setObjectName("widget")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setGeometry(QtCore.QRect(350, 10, 361, 41))
        self.widget_2.setObjectName("widget_2")
        self.pushButton_send_file = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_send_file.setGeometry(QtCore.QRect(290, 10, 71, 31))
        self.pushButton_send_file.setObjectName("pushButton_send_file")
        self.label_hq = QtWidgets.QLabel(self.widget_2)
        self.label_hq.setGeometry(QtCore.QRect(0, 4, 41, 31))
        self.label_hq.setObjectName("label_hq")
        self.lineEdit_fname = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_fname.setGeometry(QtCore.QRect(40, 10, 241, 31))
        self.lineEdit_fname.setObjectName("lineEdit_fname")
        self.textBrowser_log = QtWidgets.QTextBrowser(self.widget)
        self.textBrowser_log.setGeometry(QtCore.QRect(10, 90, 331, 301))
        self.textBrowser_log.setObjectName("textBrowser_log")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(10, 60, 71, 31))
        self.label.setObjectName("label")
        self.widget_3 = QtWidgets.QWidget(self.widget)
        self.widget_3.setGeometry(QtCore.QRect(10, 10, 331, 51))
        self.widget_3.setObjectName("widget_3")
        self.label_recv = QtWidgets.QLabel(self.widget_3)
        self.label_recv.setGeometry(QtCore.QRect(0, 10, 61, 21))
        self.label_recv.setObjectName("label_recv")
        self.lineEdit = QtWidgets.QLineEdit(self.widget_3)
        self.lineEdit.setGeometry(QtCore.QRect(50, 10, 131, 27))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget_3)
        self.lineEdit_2.setGeometry(QtCore.QRect(190, 10, 51, 27))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.widget_my = myQWidget(self.widget)
        self.widget_my.setGeometry(QtCore.QRect(350, 80, 361, 351))
        self.widget_my.setObjectName("widget_my")


        self.widget_4 = QtWidgets.QWidget(self.widget)
        self.widget_4.setGeometry(QtCore.QRect(0, 400, 341, 31))
        self.widget_4.setObjectName("widget_4")
        self.pushButton_send_msg = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_send_msg.setGeometry(QtCore.QRect(280, 0, 61, 31))
        self.pushButton_send_msg.setObjectName("pushButton_send_msg")

        self.lineEdit_fname_msg = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_fname_msg.setGeometry(QtCore.QRect(10, 0, 271, 31))
        self.lineEdit_fname_msg.setObjectName("lineEdit_fname_msg")

        self.tabWidget.addTab(self.widget, "")
        self.content_2 = QtWidgets.QWidget()
        self.content_2.setEnabled(False)
        self.content_2.setObjectName("content_2")
        self.tabWidget.addTab(self.content_2, "")
        self.widget_head = QtWidgets.QWidget(self.centralwidget)
        self.widget_head.setGeometry(QtCore.QRect(0, 0, 721, 41))
        self.widget_head.setObjectName("widget_head")
        self.pushButton_log = QtWidgets.QPushButton(self.widget_head)
        self.pushButton_log.setGeometry(QtCore.QRect(640, 0, 81, 41))
        self.pushButton_log.setObjectName("pushButton_log")
        self.label_head_user = QtWidgets.QLabel(self.widget_head)
        self.label_head_user.setGeometry(QtCore.QRect(560, 10, 68, 21))
        self.label_head_user.setObjectName("label_head_user")
        self.widget_head_2 = QtWidgets.QWidget(self.widget_head)
        self.widget_head_2.setGeometry(QtCore.QRect(260, 0, 261, 41))
        self.widget_head_2.setObjectName("widget_head_2")
        self.label_time = QtWidgets.QLabel(self.widget_head_2)
        self.label_time.setGeometry(QtCore.QRect(0, 0, 68, 41))
        self.label_time.setObjectName("label_time")
        self.label_time_content = QtWidgets.QLabel(self.widget_head_2)
        self.label_time_content.setGeometry(QtCore.QRect(70, 0, 151, 41))
        self.label_time_content.setObjectName("label_time_content")
        self.widget_head_1 = QtWidgets.QWidget(self.widget_head)
        self.widget_head_1.setGeometry(QtCore.QRect(0, 0, 191, 41))
        self.widget_head_1.setObjectName("widget_head_1")
        self.label_about = QtWidgets.QLabel(self.widget_head_1)
        self.label_about.setGeometry(QtCore.QRect(10, 0, 41, 41))
        self.label_about.setObjectName("label_about")
        self.label_help = QtWidgets.QLabel(self.widget_head_1)
        self.label_help.setGeometry(QtCore.QRect(50, 0, 41, 41))
        self.label_help.setObjectName("label_help")

        self.widget_5 = QtWidgets.QWidget(self.centralwidget)
        self.widget_5.setGeometry(QtCore.QRect(0, 520, 711, 31))
        self.widget_5.setObjectName("widget_5")

        self.label_scroll = scrollTextLabel(self.widget_5)
        self.label_scroll.setGeometry(QtCore.QRect(80, 0, 631, 31))
        self.label_scroll.setObjectName("label_scroll")

        self.label_3 = QtWidgets.QLabel(self.widget_5)
        self.label_3.setGeometry(QtCore.QRect(10, 0, 71, 31))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "飞鸽传输"))
        self.tabWidget.setToolTip(_translate("MainWindow", "tcp传输"))
        self.tabWidget.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>tcp传输</p></body></html>"))
        self.pushButton_send_file.setText(_translate("MainWindow", "发送文件"))
        self.label_hq.setText(_translate("MainWindow", "文件:"))
        self.label.setText(_translate("MainWindow", "日志输出:"))
        self.label_recv.setText(_translate("MainWindow", "IP地址:"))
        self.lineEdit.setText(_translate("MainWindow", "192.168.1.104"))
        self.lineEdit_2.setText(_translate("MainWindow", "8888"))

        self.pushButton_send_msg.setText(_translate("MainWindow", "发送"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), _translate("MainWindow", "首页"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.content_2), _translate("MainWindow", "工具"))
        self.pushButton_log.setText(_translate("MainWindow", "登录/注销"))
        self.label_head_user.setText(_translate("MainWindow", ""))
        self.label_time.setText(_translate("MainWindow", "当前时间:"))
        self.label_time_content.setText(_translate("MainWindow", "2018 01-10 11.12.55"))
        self.label_about.setText(_translate("MainWindow", "关于"))
        self.label_help.setText(_translate("MainWindow", "帮助"))
        self.label_3.setText(_translate("MainWindow", "最新消息:"))
        self.label_scroll.setText(_translate("MainWindow", ""))


class myQWidget(QtWidgets.QWidget):
    fileSignal = QtCore.pyqtSignal(str)
    def __init__(self,parent=None):
        super(myQWidget, self).__init__(parent)
        #窗体背景
        self.setPalette(QtGui.QPalette(QtCore.Qt.gray))
        self.setAutoFillBackground(True)
        self.setAcceptDrops(True)
        #其他变量
        self.DirFlag=False
        self.pix = QtGui.QPixmap('../config/exe.png')
        # self.setUI()
    # def setUI(self):
        #新建窗体
        self.imageLabel = QtWidgets.QLabel(self)
        self.imageLabel.setGeometry(QtCore.QRect(130,10,121,111))

        self.fpathLabel = QtWidgets.QLabel(self)
        self.fpathLabel.setGeometry(QtCore.QRect(50,130,261,31))
        self.fpathLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.widget_file = QtWidgets.QWidget(self)
        self.widget_file.setGeometry(QtCore.QRect(10, 160, 361, 191))
        self.widget_file.setObjectName(_fromUtf8("widget_file"))

        self.label_fiel_all = QtWidgets.QLabel(self.widget_file)
        self.label_fiel_all.setGeometry(QtCore.QRect(0, 0, 71, 31))
        self.label_fiel_all.setObjectName(_fromUtf8("label_fiel_all"))

        self.label_size = QtWidgets.QLabel(self.widget_file)
        self.label_size.setGeometry(QtCore.QRect(30, 60, 41, 31))
        self.label_size.setObjectName(_fromUtf8("label_size"))

        self.label_path = QtWidgets.QLabel(self.widget_file)
        self.label_path.setGeometry(QtCore.QRect(30, 30, 41, 31))
        self.label_path.setObjectName(_fromUtf8("label_path"))

        self.label_auth = QtWidgets.QLabel(self.widget_file)
        self.label_auth.setGeometry(QtCore.QRect(30, 90, 41, 31))
        self.label_auth.setObjectName(_fromUtf8("label_auth"))

        self.label_sum = QtWidgets.QLabel(self.widget_file)
        self.label_sum.setGeometry(QtCore.QRect(0, 120, 71, 31))
        self.label_sum.setObjectName(_fromUtf8("label_sum"))

        self.label_bar_info = QtWidgets.QLabel(self.widget_file)
        self.label_bar_info.setGeometry(QtCore.QRect(0, 160, 71, 31))
        self.label_bar_info.setObjectName("label_bar_info")

        self.label_path_2 = QtWidgets.QLabel(self.widget_file)
        self.label_path_2.setGeometry(QtCore.QRect(70, 30, 261, 31))
        self.label_path_2.setObjectName(_fromUtf8("label_path_2"))

        self.label_size_2 = QtWidgets.QLabel(self.widget_file)
        self.label_size_2.setGeometry(QtCore.QRect(70, 60, 261, 31))
        self.label_size_2.setObjectName(_fromUtf8("label_size_2"))

        self.label_auth_2 = QtWidgets.QLabel(self.widget_file)
        self.label_auth_2.setGeometry(QtCore.QRect(70, 90, 261, 31))
        self.label_auth_2.setObjectName(_fromUtf8("label_auth_2"))

        self.label_sum_2 = QtWidgets.QLabel(self.widget_file)
        self.label_sum_2.setGeometry(QtCore.QRect(70, 120, 261, 31))
        self.label_sum_2.setObjectName(_fromUtf8("label_sum_2"))

        self.progressBa_send = QtWidgets.QProgressBar(self.widget_file)
        self.progressBa_send.setGeometry(QtCore.QRect(70, 170, 281, 16))
        self.progressBa_send.setProperty("value", 10)
        self.progressBa_send.setObjectName("progressBa_send")

        self.initUI()
        # 窗口标题
        # 定义窗口大小
        # self.resize(500, 400)
    def initUI(self):
        self.widget_file.setVisible(False)
        #调用Drops方法
        self.imageLabel.setText("")
        self.fpathLabel.setText(_fromUtf8('请将文件拖入此区域'))

    # 鼠标 拖入 事件
    def dragEnterEvent(self, evn):#
        filepath=self.getFilePath(evn)
        if self.isIsDir(filepath):
            self.DirFlag=True
            evn.ignore()
            return
        else:
            evn.accept()
        self.fpathLabel.setText(_fromUtf8('鼠标拖入了'))
 
    # 鼠标放开执行
    def dropEvent(self, evn):
        if self.DirFlag:
            evn.ignore()
            return
        else:
            evn.accept()
        self.fpathLabel.setText(_fromUtf8('鼠标放开了!'))
        self.setwidgetUI()
        filepath=self.getFilePath(evn)
        self.setFileInformation(_fromUtf8(filepath))
        self.DirFlag=False

    # 鼠标移动函数事件
    def dragMoveEvent(self,evn):
        if self.DirFlag:
            evn.ignore()
            return
        else:
            evn.accept()
        self.fpathLabel.setText(_fromUtf8('鼠标移动了'))

    def dragLeaveEvent(self,env):#鼠标离开
        self.DirFlag=False

    def isIsDir(self,filename):
        if not filename:
            return True
        if QtCore.QFileInfo(filename).isDir():
            return True
        return False
        
    def getFilePath(self,evn):
        py_str=_toUTF8(evn.mimeData().text())
        # MacOS
        osname = platform.system()
        # Linux
        txt_path=""
        if(osname =="Windows"):# Windows
            txt_path = py_str.replace('file:///', '')
        elif(osname == "MAC"):
            txt_path = py_str.replace('file:///', '/')
        else:
            txt_path = py_str.replace('file:///', '/').strip()
        return txt_path
    def clearFileInfo(self):
        self.initUI()
    # QString
    def setwidgetUI(self):
        self.imageLabel.setStyleSheet("border: 0px solid gray")
        self.imageLabel.setPixmap(self.pix)
        self.imageLabel.setScaledContents(True)
        self.widget_file.setVisible(True)
    # def filetypes(self,fileName):
    #     import filetype
    #     print(fileName)
    #     kind = filetype.guess(fileName)
    #     if kind is None:
    #         print('Cannot guess file type!')
    #         return
    #     print('File extension: %s' % kind.extension)
    #     print('File MIME type: %s' % kind.mime)
    def setFileInformation(self,filename):
            if not filename:
                return
            info = QtCore.QFileInfo(filename)
            if info.isDir():
                return
            self.fileSignal.emit(filename)
            # self.filetypes(filename)
            qfilepath=info.absolutePath()#不带文件名
            qfilename=info.fileName()
            qsize = info.size()
            # qcreated = info.created()
            qlastModified = info.lastModified()
            # qlastRead = info.lastRead()
            # qisDir = info.isDir()
            # qisFile = info.isFile()
            qisSymlink = info.isSymLink()
            # qisHidden = info.isHidden()
            qisReadable = info.isReadable()
            qisWritable = info.isWritable()
            qisExecutable = info.isExecutable()
            # fname,fileext = os.path.splitext(fullflname)
            qlastsize=self.GetSizeFormat(qsize)
            qlastauto=self.GetMode(qisSymlink,qisReadable,qisWritable,qisExecutable)
            qlasttime=self.TimeStampToTime(qlastModified)

            self.label_fiel_all.setText(_fromUtf8("文件详情:"))
            self.label_size.setText(_fromUtf8("大小:"))
            self.label_path.setText(_fromUtf8("路径:"))
            self.label_auth.setText(_fromUtf8("权限:"))
            self.label_sum.setText(_fromUtf8("最后修改:"))            
            self.label_bar_info.setText(_fromUtf8("传输进度:"))
            
            self.label_path_2.setText(qfilepath)
            self.label_size_2.setText(qlastsize)
            self.label_auth_2.setText(qlastauto)
            self.label_sum_2.setText(qlasttime)
            self.progressBa_send.setValue(0)
            self.progressBa_send.hide()
            #other file
            if len(qfilename)>38:
                qfilename=qfilename[:20]+"..."+qfilename[-10:]
            self.fpathLabel.setText(qfilename)
    def TimeStampToTime(self,timestamp):
        return timestamp.toString("yyyy-MM-dd hh:mm:ss");
    def GetSizeFormat(self,filesize):
        import decimal
        fsize=filesize
        funit="B"
        if fsize>=1000:
            fsize/=1000
            funit="KB"
        if fsize>=1000:
            fsize/=1000
            funit="MB"
        if fsize>=1000:
            fsize/=1000
            funit="GB"
        qstr=str(int(fsize*100)/100)+str(funit)
        return qstr
        
    def GetMode(self,qisSymlink,qisReadable,qisWritable,qisExecutable):
        auto=""
        if qisSymlink:
            auto+="链接文件,"
        if qisReadable:
            auto+="可读,"
        if qisWritable:
            auto+="可写,"
        if qisExecutable:
            auto+="可执行,"
        return _fromUtf8(auto[0:len(auto)-1])

# 自定义label
class scrollTextLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(scrollTextLabel, self).__init__(parent)
        # self.setPalette(QtGui.QPalette(QtCore.Qt.gray))
        # self.setAutoFillBackground(True)
        self.txt =_fromUtf8("")
        self.newX = 10      
        self.t = QtCore.QTimer()
        self.font =QtGui.QFont(_fromUtf8('微软雅黑, verdana'), 10)
        self.t.timeout.connect(self.changeTxtPosition)

    def changeTxtPosition(self):
        # print 'change'
        if not self.parent().isVisible():
            # 如果parent不可见，则停止滚动，复位
            self.t.stop()
            self.newX = 10
            return
        if self.textRect.width() + self.newX > 0:
        #每次向前滚动5像素
            self.newX -= 5
        else:
            self.newX = self.width()            
        self.update()

    #用drawText来绘制文字，不再需要setText，重写
    def setText(self, s):
        # print 'set text'
        self.txt = s

        #滚动起始位置设置为10,留下视觉缓冲
        #以免出现 “没注意到第一个字是什么” 的情况
        self.newX = self.width()-50
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(self.font)
        #设置透明颜色
        painter.setPen(QtGui.QColor('transparent'));

        #以透明色绘制文字，来取得绘制后的文字宽度
        self.textRect = painter.drawText(QtCore.QRect(0, -7, self.width(), 41), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, self.txt)
        # print self.textRect.width(), self.width(),self.newX
        if self.textRect.width()+self.newX>0:
            #如果绘制文本宽度大于控件显示宽度，准备滚动：
            painter.setPen(QtGui.QColor(0, 0, 0, 255))
            painter.drawText(QtCore.QRect(self.newX, -7, self.textRect.width(), 41), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, self.txt)
            #每150ms毫秒滚动一次
            self.t.start(500)
        else:
            #如果绘制文本宽度小于控件宽度，不需要滚动，文本居中对齐
            painter.setPen(QtGui.QColor(255, 255, 255, 255));
            self.textRect = painter.drawText(QtCore.QRect(0, -7, self.width(), 41), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, self.txt)
            self.t.stop()