# -*- coding: utf-8 -*-
__author__ = "gwyang@yahoo.com"

import sys, os
import time
import concurrent.futures as concur

from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMenu, QAction
from PyQt5.QtWidgets import QTreeWidgetItem, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, QThreadPool, QRunnable
from PyQt5.QtGui import QCursor, QColor, QPalette

from main_ui import *
import backend
from backend import folder

DEBUG = True

######################################
# TODO 1.Change file tree to nested list (Use class <folder>, method: <get_children, enter_child, back>;
# TODO 2.add "new folder", "copy", "paste" and "delete";
# TODO 3.add "folder icon";  [0.5/1]
# TODO 4.delete "status in fileTree";
# TODO 5.add "download" and "upload"
######################################

class WFMShelf(QMainWindow, Ui_MainWindow):

    fileSig = pyqtSignal(list)
    serverSig = pyqtSignal(list)

    def __init__(self, title="", max_process_num=None, max_thread_num = None, *args, **kwargs):
        super(WFMShelf, self).__init__(*args, **kwargs)

        # The activated item in file tree
        self.selectedFile = None

        # Setup UI
        self.setupUi(self)

        # Title of the main window
        self.setTitle(title)

        # Icon of application
        iconMain = QtGui.QIcon()
        iconMain.addPixmap(QtGui.QPixmap("icons/gnu.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(iconMain)

        # No window frame
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Global StyleSheet
        self.style = """ 
                        QPushButton{ background-color:#E0E0E0; color:#E0E0E0; } 
                        QTabWidget{ background:#E0E0E0; color:#E0E0E0; }
                        QTreeWidget{ background:#ADADAD;  }
                    """
        self.setStyleSheet(self.style)

        ###########################
        # Start keep_refreshing
        # TODO: make fileTree and serverList refresh each period
        # threadPool.submit(self.keepFileRefreshing)
        # threadPool.submit(self.kee
        ########################

        # Background of window
        totalPlatte = QPalette()
        ## totalPlatte.setColor(self.backgroundRole(), QColor(192, 253, 123))
        totalPlatte.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('icons/afu.jpg')))
        self.setPalette(totalPlatte)

        # Configure FileTree
        self.currentFileNode = folder.Folder(1, "root")
        self.file_refresh()

        self.iconTag = "/:ICON_TAG:/ "
        self.folderIcon = "icons/folder.ico"
        self.fileIcon = "icons/file.ico"

        # Current file list
        self.currentFileList = None

        # File to be copy
        self.copiedItem = None

        self.cutFlag = False

        # Rightmenu of file tree
        self.fileTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.createFileTreeRightMenu()

        # Global process pool
        self.processPool = concur.ProcessPoolExecutor(max_workers=max_process_num)
        self.threadPool = concur.ThreadPoolExecutor(max_workers=max_thread_num)

        ##########################################
        # Global rocess locker
        # when serverlist or fileTree is refreshing,
        # changes( upload, download, copy, paste, delete)
        # for file is not allowed
        self.processLockers = []

        # Cuztomized signal for show fileTree and serverTree
        self.fileSig[list].connect(self.showFileTree)
        self.serverSig[list].connect(self.showServerTree)

    ##############################################
    # *   The following three functions are events
    # when dragging the window, the main window is
    # moved to the position of arrow as a result.
    # *   This is used for non-frame window in Qt.
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
    ##############################################

    def file_item_change(self, item):
        if DEBUG:
            if item is not None:
                print('activited item change to: ', item.text(0))
            else:
                print('activited item change to: ', 'None')
        self.selectedFile = item

    def setTitle(self, title):
        if title:
            self.setWindowTitle(title)
        return self

    def lock_warning(self, msg, wait_time=0.8):
        self.statusBar().showMessage(message=msg)
        time.wait(wait_time)

        if len(self.processLockers) == 1:
            if self.processLockers[0] == "file_locker":
                self.statusBar().showMessage("file refreshing...")
            elif self.processLockers[1] == "server_locker":
                self.statusBar().showMessage("server refreshing...")
        elif len(self.processLockers) == 2:
            self.statusBar().showMessage("file and server refreshing...")



    def file_download(self):
        if self.selectedFile is not None:
            file_path, ok = QFileDialog.getSaveFileName(self,
                                                         "文件保存",
                                                         "~",
                                                         "All Files (*)")
            if ok != "":
                fileName = self.selectedFile.text(0)
                if len(self.processLockers) == 0:
                    if DEBUG:
                        print('start download: ', self.selectedFile.text(0))
                        print('            to: ', file_path)

                    self.processPool.submit()
                else:
                    if DEBUG:
                        print("information refreshing, cannot download")
                    self.threadPool.submit(self.lock_warning, "Infomation refreshing, cannot download now")

    def file_upload(self):
        pass

    def download_succeed(self, item, status={'msg': 'succeed'}):
        if status['msg'] == 'succeed':
            # item = status['file_status']
            item.setText(1, u'已下载')
            self.statusBar().showMessage('Succeed')
        else:
            self.statusBar().showMessage(status['msg'])

        self.activated = False

    def file_copy(self):
        name = self.selectedFile.text(0)
        for item in self.currentFileList:
            if item['name'] == name:
                self.curFlag = False
                self.copiedItem = item

        if DEBUG:
            print("COPY, ", )
            if self.copiedItem == None:
                print("no selected file")
            else:
                print("selected file: ", self.copiedItem['name'])

    def file_cut(self):
        name = self.selectedFile.text(0)
        for item in self.currentFileList:
            if item['name'] == name:
                self.cutFlag = True
                self.copiedItem = item

        if DEBUG:
            print("CUT, ", )
            if self.copiedItem == None:
                print("no selected file")
            else:
                print("selected file: ", self.copiedItem['name'])

    def file_paste(self):
        if DEBUG:
            print("PASTE: from ", self.copiedItem['name'], " to ", self.currentFileNode.name)

        self.threadPool.submit(self.file_paste_method)

    def file_paste_method(self):
        self.currentFileNode.paste(self.copiedItem)
        if self.cutFlag:
            self.file_delete_method(self.copiedItem)

            if DEBUG:
                print("CUTED ", self.copiedItem['name'])

        self.file_refresh_thread()

    def file_delete(self):
        if self.selectedFile != None:
            name = self.selectedFile.text(0)
            msgBox = QMessageBox(QMessageBox.Warning,
                                 "QMessageBox.warning()",
                                 "确定删除文件 " + name + " ？",
                                 QMessageBox.Yes | QMessageBox.No,
                                 self)
            if msgBox == QMessageBox.Yes:
                if DEBUG:
                    print("DELETE ", name)
                deletedItem = None
                for item in self.currentFileList:
                    if item['name'] == name:
                        deletedItem = item
                self.threadPool.submit(self.file_delete_method, deletedItem)

    def file_delete_method(self, deletedItem):
        folder.Folder.delete(deletedItem)
        self.file_refresh_thread()

    def deleteTree(self, QTree):
        """
        Make a subtree of QTreeWidget Empty
        :param QTree: QTreeWidget
        :return: None
        """
        num = QTree.topLevelItemCount()
        while num != 0:
            QTree.takeTopLevelItem(0)
            num = QTree.topLevelItemCount()

    def addChildren(self, root, itemList, names):
        """
        add items in list to a node of QTreeWidget as children
        :param root: node to add children
        :param itemList: list of nodes to be added
        :param names: names in the QTreeWidget
        :return: None
        """
        num = len(names)
        for item in itemList:
            child = QTreeWidgetItem(root)
            if item.has_key("is_folder"):
                child.setIcon(0, QtGui.QIcon(item["is_folder"][len(self.iconTag):]))
            for i in range(num):
                child.setText(i, item[names[i]])

            if "children" in item:
                self.addChildren(child, item["children"], names)

    def showServerTree(self, serverTree):
        self.deleteTree(self.serverTree)
        self.addChildren(self.serverTree,
                         serverTree,
                         ["id", "ip", "used", "remain"])

    def server_refresh_thread(self):
        self.processLockers.append("server_locker")

        if self.statusBar().currentMessage() == "file refreshing...":
            self.statusBar().showMessage("file and server refreshing...")
        else:
            self.statusBar().showMessage("server refreshing...")

        self.currentFileList = backend.server.get_server_list()
        self.serverSig[list].emit(self.currentFileList)

        if self.statusBar().currentMessage() == "server refreshing...":
            self.statusBar().showMessage("server refresh done")
            time.sleep(0.8)
            self.statusBar().showMessage("")
        elif self.statusBar().currentMessage() == "file and server refreshing...":
            self.statusBar().showMessage("file refreshing...")
        else:
            temp = self.statusBar().currentMessage()
            self.statusBar().showMessage("server refresh done")
            time.sleep(0.8)
            self.statusBar().showMessage(temp)

        # delete server_locker
        self.processLockers = list(filter(
            lambda item: item != "server_locker",
            self.processLockers
        ))

    def server_refresh(self):
        if DEBUG:
            print("server refresh")

        if not ("server_locker" in self.processLockers):
            threadPool = concur.ThreadPoolExecutor()
            threadPool.submit(self.server_refresh_thread)

    def showFileTree(self, fileTree):
        self.deleteTree(self.fileTree)
        self.addChildren(self.fileTree,
                          fileTree,
                          ["name", "size", "date"])

    def file_refresh_thread(self):
        self.processLockers.append("file_locker")

        if self.statusBar().currentMessage() == "server refreshing...":
            self.statusBar().showMessage("file and server refreshing...")
        else:
            self.statusBar().showMessage("file refreshing...")

        fileList = self.currentFileNode.get_children()
        if self.currentFileList.id != 1:
            fileList.insert(0, {"is_folder": True,
                                "name": "..",
                                "size": "",
                                "date": ""})
        for item in fileList:
            if item["is_folder"]:
                item["is_folder"] = self.iconTag + self.folderIcon
            else:
                item["is_folder"] = self.iconTag + self.fileIcon
        self.fileSig[list].emit(fileList)

        if self.statusBar().currentMessage() == "file refreshing...":
            self.statusBar().showMessage("file refresh done")
            time.sleep(0.8)
            self.statusBar().showMessage("")
        elif self.statusBar().currentMessage() == "file and server refreshing...":
            self.statusBar().showMessage("server refreshing...")
        else:
            temp = self.statusBar().currentMessage()
            self.statusBar().showMessage("file refresh done")
            time.sleep(0.8)
            self.statusBar().showMessage(temp)

        # delete file_locker
        self.processLockers = list(filter(
            lambda item: item != "file_locker",
            self.processLockers
        ))

    def file_refresh(self):
        if DEBUG:
            print("file refresh")

        if not ("file_locker" in self.processLockers):
            threadPool = concur.ThreadPoolExecutor()
            threadPool.submit(self.file_refresh_thread)

    def enter_folder(self):
        subFolder = self.selectedFile.text(1)
        if subFolder == "..":
            if self.currentFileNode.id != 1:
                self.currentFileNode.go_back()
        else:
            if self.selectedFile.icon(0) == self.iconTag + self.folderIcon:
                self.currentFileNode.enter_folder(subFolder)
        self.file_refresh()

    def go_back(self):
        if self.currentFileNode.id != 1:
            self.currentFileNode.go_back()
        self.file_refresh()

    def new_folder(self):
        name, ok = QInputDialog.getText(self, "新建文件夹", "文件夹名: ", QLineEdit.Normal, "")
        if ok:
            newItem = QTreeWidgetItem(self.fileTree)
            newItem.setIcon(0, QtGui.QIcon(self.folderIcon))
            newItem.setText(0, name)
            newItem.setText(1, "")
            newItem.setText(2, "")
            self.fileTree.addTopLevelItem(newItem)

            self.currentFileNode.new_folder(name)
            self.file_refresh()

    ##############################################
    # *   Creat right menu for fileTree
    def file_context(self, point):
        if self.selectedFile is not None:
            self.fileTreeRightMenu.exec_(QCursor.pos())
            self.fileTreeRightMenu.show()

    def createFileTreeRightMenu(self):
        self.fileTreeRightMenu = QMenu(self.fileTree)

        downAction = QAction(QtGui.QIcon("icons/download.ico"), u"&下载", self)
        downAction.triggered.connect(self.file_download)
        self.fileTreeRightMenu.addAction(downAction)

        backAction = QAction(QtGui.QIcon("icons/back.ico"), u"&后退", self)
        backAction.setShortcut("Ctrl+B")
        backAction.triggered.connect(self.go_back)
        self.fileTreeRightMenu.addAction(backAction)

        newAction = QAction(QtGui.QIcon("icons/newFolder.ico"), u"&新建文件夹", self)
        newAction.setShortcut("Ctrl+N")
        newAction.triggered.connect(self.new_folder)
        self.fileTreeRightMenu.addAction(newAction)

        refreshAction = QAction(QtGui.QIcon("icons/refresh.ico"), u"&刷新", self)
        refreshAction.setShortcut("F5")
        refreshAction.triggered.connect(self.file_refresh)
        self.fileTreeRightMenu.addAction(refreshAction)

        self.fileTreeRightMenu.addSeparator()

        copyAction = QAction(QtGui.QIcon("icons/copy.ico"), u"&复制", self)
        copyAction.setShortcut("Ctrl+C")
        copyAction.triggered.connect(self.file_copy)
        self.fileTreeRightMenu.addAction(copyAction)

        pasteAction = QAction(QtGui.QIcon("icons/paste.ico"), u"&粘贴", self)
        pasteAction.setShortcut("Ctrl+V")
        pasteAction.triggered.connect(self.file_paste)
        self.fileTreeRightMenu.addAction(pasteAction)

        cutAction = QAction(QtGui.QIcon("icons/cut.ico"), u"&剪切", self)
        cutAction.setShortcut("Ctrl+X")
        cutAction.triggered.connect(self.file_cut)
        self.fileTreeRightMenu.addAction(cutAction)

        deleteAction = QAction(QtGui.QIcon("icons/close.ico"), u"&删除", self)
        deleteAction.setShortcut("Ctrl+D")
        deleteAction.triggered.connect(self.file_delete)
        self.fileTreeRightMenu.addAction(deleteAction)
    ##########################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wfm_shelf = WFMShelf(title="Futanari Distributed File Syetem")
    wfm_shelf.show()
    sys.exit(app.exec_())
