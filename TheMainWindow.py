# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TheMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(20, 30, 761, 531))
        self.treeView.setObjectName("treeView")
        self.newFolderButton = QtWidgets.QPushButton(self.centralwidget)
        self.newFolderButton.setGeometry(QtCore.QRect(20, 0, 113, 32))
        self.newFolderButton.setObjectName("newFolderButton")
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setGeometry(QtCore.QRect(380, 0, 113, 32))
        self.deleteButton.setObjectName("deleteButton")
        self.logOutButton = QtWidgets.QPushButton(self.centralwidget)
        self.logOutButton.setGeometry(QtCore.QRect(670, 0, 113, 32))
        self.logOutButton.setObjectName("logOutButton")
        self.moveVideoButton = QtWidgets.QPushButton(self.centralwidget)
        self.moveVideoButton.setGeometry(QtCore.QRect(140, 0, 113, 32))
        self.moveVideoButton.setObjectName("moveVideoButton")
        self.updateButton = QtWidgets.QPushButton(self.centralwidget)
        self.updateButton.setGeometry(QtCore.QRect(550, 0, 113, 32))
        self.updateButton.setObjectName("updateButton")
        self.editTitleButton = QtWidgets.QPushButton(self.centralwidget)
        self.editTitleButton.setGeometry(QtCore.QRect(260, 0, 113, 32))
        self.editTitleButton.setObjectName("editTitleButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.newFolderButton.setText(_translate("MainWindow", "New folder"))
        self.deleteButton.setText(_translate("MainWindow", "Delete"))
        self.logOutButton.setText(_translate("MainWindow", "Log out"))
        self.moveVideoButton.setText(_translate("MainWindow", "Move video.."))
        self.updateButton.setText(_translate("MainWindow", "Update"))
        self.editTitleButton.setText(_translate("MainWindow", "Edit title"))