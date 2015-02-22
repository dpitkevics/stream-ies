# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Daniels\Documents\QtUi-s\stream-ies-mainwindow.ui'
#
# Created: Sun Feb 22 21:26:47 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../PycharmProjects/stream-ies/resources/images/icon2-150x150.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.search_query = QtGui.QLineEdit(self.centralwidget)
        self.search_query.setGeometry(QtCore.QRect(0, 0, 731, 20))
        self.search_query.setObjectName("search_query")
        self.search_button = QtGui.QPushButton(self.centralwidget)
        self.search_button.setGeometry(QtCore.QRect(725, -2, 75, 23))
        self.search_button.setObjectName("search_button")
        self.scroll_layout = QtGui.QScrollArea(self.centralwidget)
        self.scroll_layout.setGeometry(QtCore.QRect(0, 20, 801, 461))
        self.scroll_layout.setWidgetResizable(True)
        self.scroll_layout.setObjectName("scroll_layout")
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 799, 459))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scroll_layout.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Stream-Ies", None, QtGui.QApplication.UnicodeUTF8))
        self.search_button.setText(QtGui.QApplication.translate("MainWindow", "Search", None, QtGui.QApplication.UnicodeUTF8))

