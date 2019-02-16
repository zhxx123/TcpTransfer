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
from myGui import *
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
