# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1288, 690)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.China))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.China))
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(250, 40, 1011, 621))
        self.tabWidget.setToolTipDuration(1)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.China))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(32, 32))
        self.tabWidget.setObjectName("tabWidget")
        self.fileView = QtWidgets.QWidget()
        self.fileView.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.China))
        self.fileView.setObjectName("fileView")
        self.fileTree = QtWidgets.QTreeWidget(self.fileView)
        self.fileTree.setEnabled(True)
        self.fileTree.setGeometry(QtCore.QRect(0, 120, 1011, 471))
        self.fileTree.setObjectName("fileTree")
        self.fileTree.header().setDefaultSectionSize(220)
        self.fileTree.header().setSortIndicatorShown(True)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.fileView)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(200, 10, 459, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.fileButtons = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.fileButtons.setContentsMargins(0, 0, 0, 0)
        self.fileButtons.setSpacing(4)
        self.fileButtons.setObjectName("fileButtons")
        self.uploadButton = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uploadButton.sizePolicy().hasHeightForWidth())
        self.uploadButton.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/upload.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.uploadButton.setIcon(icon)
        self.uploadButton.setIconSize(QtCore.QSize(32, 32))
        self.uploadButton.setObjectName("uploadButton")
        self.fileButtons.addWidget(self.uploadButton)
        self.downloadButton = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/download.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downloadButton.setIcon(icon1)
        self.downloadButton.setIconSize(QtCore.QSize(32, 32))
        self.downloadButton.setObjectName("downloadButton")
        self.fileButtons.addWidget(self.downloadButton)
        self.newFolderButton = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/new_folder.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.newFolderButton.setIcon(icon2)
        self.newFolderButton.setIconSize(QtCore.QSize(34, 34))
        self.newFolderButton.setObjectName("newFolderButton")
        self.fileButtons.addWidget(self.newFolderButton)
        self.toolButton = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/rename.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon3)
        self.toolButton.setIconSize(QtCore.QSize(32, 32))
        self.toolButton.setObjectName("toolButton")
        self.fileButtons.addWidget(self.toolButton)
        self.copyButton = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/copy.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.copyButton.setIcon(icon4)
        self.copyButton.setIconSize(QtCore.QSize(32, 32))
        self.copyButton.setObjectName("copyButton")
        self.fileButtons.addWidget(self.copyButton)
        self.pasteButton = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/paste.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pasteButton.setIcon(icon5)
        self.pasteButton.setIconSize(QtCore.QSize(32, 32))
        self.pasteButton.setObjectName("pasteButton")
        self.fileButtons.addWidget(self.pasteButton)
        self.cutButton = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/cut.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cutButton.setIcon(icon6)
        self.cutButton.setIconSize(QtCore.QSize(32, 32))
        self.cutButton.setObjectName("cutButton")
        self.fileButtons.addWidget(self.cutButton)
        self.deleteButton = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icons/close.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(icon7)
        self.deleteButton.setIconSize(QtCore.QSize(32, 32))
        self.deleteButton.setObjectName("deleteButton")
        self.fileButtons.addWidget(self.deleteButton)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.fileView)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(30, 10, 121, 61))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.goBackButton = QtWidgets.QToolButton(self.horizontalLayoutWidget_3)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icons/back.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.goBackButton.setIcon(icon8)
        self.goBackButton.setIconSize(QtCore.QSize(36, 36))
        self.goBackButton.setObjectName("goBackButton")
        self.horizontalLayout_2.addWidget(self.goBackButton)
        self.fileRefreshButton = QtWidgets.QToolButton(self.horizontalLayoutWidget_3)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("icons/refresh.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fileRefreshButton.setIcon(icon9)
        self.fileRefreshButton.setIconSize(QtCore.QSize(32, 32))
        self.fileRefreshButton.setObjectName("fileRefreshButton")
        self.horizontalLayout_2.addWidget(self.fileRefreshButton)
        self.currentPathLine = QtWidgets.QLineEdit(self.fileView)
        self.currentPathLine.setEnabled(True)
        self.currentPathLine.setGeometry(QtCore.QRect(130, 80, 631, 31))
        self.currentPathLine.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.currentPathLine.setText("")
        self.currentPathLine.setReadOnly(True)
        self.currentPathLine.setClearButtonEnabled(False)
        self.currentPathLine.setObjectName("currentPathLine")
        self.label = QtWidgets.QLabel(self.fileView)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(30, 80, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.tabWidget.addTab(self.fileView, "")
        self.taskView = QtWidgets.QWidget()
        self.taskView.setObjectName("taskView")
        self.taskTree = QtWidgets.QTreeWidget(self.taskView)
        self.taskTree.setGeometry(QtCore.QRect(0, 0, 1011, 591))
        self.taskTree.setLineWidth(1)
        self.taskTree.setObjectName("taskTree")
        self.taskTree.header().setDefaultSectionSize(200)
        self.taskTree.header().setSortIndicatorShown(True)
        self.tabWidget.addTab(self.taskView, "")
        self.serverView = QtWidgets.QWidget()
        self.serverView.setObjectName("serverView")
        self.serverRefreshButton = QtWidgets.QPushButton(self.serverView)
        self.serverRefreshButton.setGeometry(QtCore.QRect(930, 10, 51, 51))
        self.serverRefreshButton.setText("")
        self.serverRefreshButton.setIcon(icon9)
        self.serverRefreshButton.setIconSize(QtCore.QSize(48, 48))
        self.serverRefreshButton.setObjectName("serverRefreshButton")
        self.serverTree = QtWidgets.QTreeWidget(self.serverView)
        self.serverTree.setGeometry(QtCore.QRect(0, 60, 1001, 531))
        self.serverTree.setIndentation(20)
        self.serverTree.setRootIsDecorated(True)
        self.serverTree.setUniformRowHeights(True)
        self.serverTree.setObjectName("serverTree")
        self.serverTree.header().setCascadingSectionResizes(False)
        self.serverTree.header().setDefaultSectionSize(150)
        self.serverTree.header().setHighlightSections(False)
        self.serverTree.header().setSortIndicatorShown(True)
        self.serverTree.header().setStretchLastSection(True)
        self.tabWidget.addTab(self.serverView, "")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(1180, 0, 98, 51))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.minimizedButton = QtWidgets.QToolButton(self.horizontalLayoutWidget_2)
        self.minimizedButton.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("icons/minimize.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.minimizedButton.setIcon(icon10)
        self.minimizedButton.setIconSize(QtCore.QSize(32, 32))
        self.minimizedButton.setObjectName("minimizedButton")
        self.horizontalLayout.addWidget(self.minimizedButton)
        self.closeButton = QtWidgets.QToolButton(self.horizontalLayoutWidget_2)
        self.closeButton.setText("")
        self.closeButton.setIcon(icon7)
        self.closeButton.setIconSize(QtCore.QSize(32, 32))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.closeButton.clicked.connect(MainWindow.close)
        self.minimizedButton.clicked.connect(MainWindow.showMinimized)
        self.uploadButton.clicked.connect(MainWindow.file_upload)
        self.downloadButton.clicked.connect(MainWindow.file_download)
        self.copyButton.clicked.connect(MainWindow.file_copy)
        self.pasteButton.clicked.connect(MainWindow.file_paste)
        self.deleteButton.clicked.connect(MainWindow.file_delete)
        self.fileRefreshButton.clicked.connect(MainWindow.file_refresh)
        self.fileTree.customContextMenuRequested['QPoint'].connect(MainWindow.file_context)
        self.fileTree.currentItemChanged['QTreeWidgetItem*','QTreeWidgetItem*'].connect(MainWindow.file_item_change)
        self.serverRefreshButton.clicked.connect(MainWindow.server_refresh)
        self.newFolderButton.clicked.connect(MainWindow.new_folder)
        self.fileRefreshButton.clicked.connect(MainWindow.file_refresh)
        self.goBackButton.clicked.connect(MainWindow.go_back)
        self.fileTree.itemDoubleClicked['QTreeWidgetItem*','int'].connect(MainWindow.enter_folder)
        self.cutButton.clicked.connect(MainWindow.file_cut)
        self.toolButton.clicked.connect(MainWindow.change_name)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.fileTree.headerItem().setText(0, _translate("MainWindow", "名称"))
        self.fileTree.headerItem().setText(1, _translate("MainWindow", "大小"))
        self.fileTree.headerItem().setText(2, _translate("MainWindow", "修改日期"))
        self.uploadButton.setText(_translate("MainWindow", "上传"))
        self.downloadButton.setText(_translate("MainWindow", "下载"))
        self.newFolderButton.setText(_translate("MainWindow", "New"))
        self.toolButton.setText(_translate("MainWindow", "Rename"))
        self.copyButton.setText(_translate("MainWindow", "复制"))
        self.pasteButton.setText(_translate("MainWindow", "粘贴"))
        self.cutButton.setText(_translate("MainWindow", "Cut"))
        self.deleteButton.setText(_translate("MainWindow", "删除"))
        self.goBackButton.setText(_translate("MainWindow", "BACK"))
        self.fileRefreshButton.setText(_translate("MainWindow", "刷新"))
        self.label.setText(_translate("MainWindow", "当前路径："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.fileView), _translate("MainWindow", "文件"))
        self.taskTree.headerItem().setText(0, _translate("MainWindow", "序号"))
        self.taskTree.headerItem().setText(1, _translate("MainWindow", "文件名"))
        self.taskTree.headerItem().setText(2, _translate("MainWindow", "上传/下载"))
        self.taskTree.headerItem().setText(3, _translate("MainWindow", "进度"))
        self.taskTree.headerItem().setText(4, _translate("MainWindow", "路径"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.taskView), _translate("MainWindow", "任务"))
        self.serverTree.setSortingEnabled(True)
        self.serverTree.headerItem().setText(0, _translate("MainWindow", "编号"))
        self.serverTree.headerItem().setText(1, _translate("MainWindow", "地址"))
        self.serverTree.headerItem().setText(2, _translate("MainWindow", "已用空间"))
        self.serverTree.headerItem().setText(3, _translate("MainWindow", "剩余空间"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.serverView), _translate("MainWindow", "服务器"))

