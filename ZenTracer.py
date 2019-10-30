# -*- coding: utf-8 -*-
import base64
import json
import sys
import threading
import time
from copy import copy

import frida

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

APP = None  # type: ZenTracer

scripts = []
device = None

from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1015, 769)
        MainWindow.setMaximumSize(QtCore.QSize(16777214, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView.sizePolicy().hasHeightForWidth())
        self.treeView.setSizePolicy(sizePolicy)
        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.treeView.setExpandsOnDoubleClick(False)
        self.treeView.setObjectName("treeView")
        self.gridLayout.addWidget(self.treeView, 0, 0, 1, 1)
        self.logList = QtWidgets.QListView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logList.sizePolicy().hasHeightForWidth())
        self.logList.setSizePolicy(sizePolicy)
        self.logList.setObjectName("logList")
        self.gridLayout.addWidget(self.logList, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1015, 23))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuAction = QtWidgets.QMenu(self.menubar)
        self.menuAction.setObjectName("menuAction")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionImport_jadx_jobf = QtWidgets.QAction(MainWindow)
        self.actionImport_jadx_jobf.setObjectName("actionImport_jadx_jobf")
        self.actionExportJSON = QtWidgets.QAction(MainWindow)
        self.actionExportJSON.setObjectName("actionExportJSON")
        self.actionImportJSON = QtWidgets.QAction(MainWindow)
        self.actionImportJSON.setObjectName("actionImportJSON")
        self.actionStart = QtWidgets.QAction(MainWindow)
        self.actionStart.setObjectName("actionStart")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionBlack_Regex = QtWidgets.QAction(MainWindow)
        self.actionBlack_Regex.setObjectName("actionBlack_Regex")
        self.actionMatch_Regex = QtWidgets.QAction(MainWindow)
        self.actionMatch_Regex.setObjectName("actionMatch_Regex")
        self.actionClean = QtWidgets.QAction(MainWindow)
        self.actionClean.setObjectName("actionClean")
        self.menuMenu.addAction(self.actionExportJSON)
        self.menuMenu.addAction(self.actionImportJSON)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionImport_jadx_jobf)
        self.menuAction.addAction(self.actionStart)
        self.menuAction.addAction(self.actionClean)
        self.menuAction.addSeparator()
        self.menuAction.addAction(self.actionMatch_Regex)
        self.menuAction.addAction(self.actionBlack_Regex)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuAction.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.actionImport_jadx_jobf.triggered.connect(MainWindow.import_jobf_onClick)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ZenTracer"))
        self.menuMenu.setTitle(_translate("MainWindow", "File"))
        self.menuAction.setTitle(_translate("MainWindow", "Action"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionImport_jadx_jobf.setText(_translate("MainWindow", "Import jadx-jobf"))
        self.actionExportJSON.setText(_translate("MainWindow", "Export JSON"))
        self.actionImportJSON.setText(_translate("MainWindow", "Import JSON"))
        self.actionStart.setText(_translate("MainWindow", "Start"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionBlack_Regex.setText(_translate("MainWindow", "Black RegEx"))
        self.actionMatch_Regex.setText(_translate("MainWindow", "Match RegEx"))
        self.actionClean.setText(_translate("MainWindow", "Clean"))


class ListDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(390, 267)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.listView = QtWidgets.QListView(Dialog)
        self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listView.setAlternatingRowColors(False)
        self.listView.setObjectName("listView")
        self.gridLayout.addWidget(self.listView, 0, 0, 1, 3)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.add = QtWidgets.QPushButton(Dialog)
        self.add.setObjectName("add")
        self.gridLayout.addWidget(self.add, 1, 1, 1, 1)
        self.remove = QtWidgets.QPushButton(Dialog)
        self.remove.setObjectName("remove")
        self.gridLayout.addWidget(self.remove, 1, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.add.setText(_translate("Dialog", "add"))
        self.remove.setText(_translate("Dialog", "remove"))


def FridaReceive(message, data):
    if message['type'] == 'send':
        if message['payload'][:12] == 'ZenTracer:::':
            packet = json.loads(message['payload'][12:])
            cmd = packet['cmd']
            data = packet['data']
            if cmd == 'log':
                APP.log(data)
            elif cmd == 'enter':
                tid, tName, cls, method, args = data
                APP.method_entry(tid, tName, cls, method, args)
            elif cmd == 'exit':
                tid, retval = data
                APP.method_exit(tid, retval)
    else:
        print(message['stack'])


class TraceItem(QStandardItem):
    def __init__(self, clazz, method, args, parent_item, retval=None, *__args):
        self.method = method
        self.args = args
        self.retval = retval
        self.clazz = clazz
        self.parent_item = parent_item
        super(TraceItem, self).__init__(str(self), *__args)
        self.parent_item.appendRow(self)
        self.flush_text()

    def __str__(self):
        # s = '{}.{}({})'.format(self.clazz, self.method, self.args)
        s = '{}.{}'.format(self.clazz, self.method)
        # if self.retval is not None: s += ' ---- {}'.format(self.retval)
        return s

    def flush_text(self):
        self.setText(str(self))
        if isinstance(self.parent_item, QStandardItem):
            self.parent().setChild(self.row(), 1, QStandardItem(str(self.args)))
            self.parent().setChild(self.row(), 2, QStandardItem(str(self.retval)))
        elif isinstance(self.parent_item, QStandardItemModel):
            self.model().setItem(self.row(), 1, QStandardItem(str(self.args)))
            self.model().setItem(self.row(), 2, QStandardItem(str(self.retval)))

    def set_method(self, me):
        self.method = me
        self.flush_text()

    def set_class(self, clazz):
        self.clazz = clazz
        self.flush_text()

    def set_args(self, args):
        self.args = args
        self.flush_text()

    def set_retval(self, retval):
        self.retval = retval
        self.flush_text()


class ListWindow(QDialog):
    data = None  # type: list[str]

    def __init__(self, data, title):
        super(ListWindow, self).__init__(APP.window)
        self.data = data
        self.ui = ListDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.setupList()
        self.setupAction()

    def setupList(self):
        model = QStandardItemModel(self.ui.listView)

        self.ui.listView.setModel(model)
        data = list(set(self.data))
        for i in range(len(self.data) - len(data)):
            del self.data[0]
        for i in range(len(data)):
            self.data[i] = data[i]
            model.appendRow(QStandardItem(self.data[i]))

    def setupAction(self):
        self.ui.add.clicked.connect(self.add)
        self.ui.remove.clicked.connect(self.remove)

    def add(self):
        text = self.ui.lineEdit.text()
        if text:
            if text in self.data:
                print('[*] INFO: {} is already exits'.format(text))
                return
            self.data.append(text)
            self.ui.listView.model().appendRow(QStandardItem(text))

    def remove(self):
        if self.ui.listView.selectedIndexes():
            del self.data[self.ui.listView.selectedIndexes()[0].row()]
            self.ui.listView.model().removeRow(self.ui.listView.selectedIndexes()[0].row())


def start_trace(app):
    global scripts
    global device

    def _attach(pid):
        if not device: return
        app.log("attach '{}'".format(pid))
        session = device.attach(pid)
        session.enable_child_gating()
        source = open('trace.js', 'r').read().replace('{MATCHREGEX}', match_s).replace("{BLACKREGEX}", black_s)
        script = session.create_script(source)
        script.on("message", FridaReceive)
        script.load()
        scripts.append(script)

    def _on_child_added(child):
        _attach(child.pid)

    device = frida.get_usb_device()
    match_s = str(app.match_regex_list).replace('u\'', '\'')
    black_s = str(app.black_regex_list).replace('u\'', '\'')
    device.on("child-added", _on_child_added)
    application = device.get_frontmost_application()
    target = 'Gadget' if application.identifier == 're.frida.Gadget' else application.identifier
    for process in device.enumerate_processes():
        if target in process.name:
            _attach(process.name)


def stop_trace(app):
    global scripts
    for s in copy(scripts):
        s.unload()
        app.log("trace script unload")
        scripts.remove(s)


class ZenTracerWindow(QMainWindow):
    app = None  # type: ZenTracer

    def __init__(self, app):
        super(ZenTracerWindow, self).__init__()
        self.app = app

    def start_onClick(self):
        if scripts:
            stop_trace(self.app)
            self.app.ui.actionStart.setText("Start")
        else:
            threading.Thread(target=start_trace, args=(self.app,)).start()
            self.app.ui.actionStart.setText("Stop")

    def clean_onClick(self):
        self.app.ui.treeView.model().removeRows(0, self.app.ui.treeView.model().rowCount())
        self.app.thread_map = {}

    def about_onClick(self):
        QMessageBox().about(self.app.window, "About",
                            "\nZenTracer: Android Tracer based-on frida \nAuthor: github.com/hluwa")

    def import_jobf_onClick(self):
        jobfile = QFileDialog.getOpenFileName(self, 'import jadx job file', '', 'job file(*.jobf)')
        if isinstance(jobfile, tuple):
            jobfile = jobfile[0]
        if not jobfile:
            return
        jobbody = open(jobfile).read()
        cls_maps = {}
        for t in jobbody.splitlines():
            if t[:1] == 'c':
                src, dest = t[2:].split(' = ')
                pkg = src[:src.rindex('.') + 1]
                cls = src[src.rindex('.') + 1:]
                if "$" in cls:
                    pkg += cls[:cls.rindex('$') + 1]
                    cls = cls[cls.rindex('$') + 1:]
                cls_maps[pkg + cls] = pkg + dest
        for tid in self.app.thread_map:
            for item in self.app.thread_map[tid]['list']:
                if isinstance(item, TraceItem) and item.clazz in cls_maps:
                    item.set_class(cls_maps[item.clazz])

    def black_onClick(self):
        self.app.black_regex_dialog.show()

    def match_onClick(self):
        self.app.match_regex_dialog.show()

    def export_onClick(self):
        jobfile = QFileDialog.getSaveFileName(self, 'export', '', 'json file(*.json)')
        if isinstance(jobfile, tuple):
            jobfile = jobfile[0]
        if not jobfile:
            return
        f = open(jobfile, 'w')
        export = {}
        export['match_regex'] = self.app.match_regex_list
        export['black_regex'] = self.app.black_regex_list
        tree = {}
        for tid in self.app.thread_map:
            tree[self.app.thread_map[tid]['list'][0].text()] = gen_tree(self.app.thread_map[tid]['list'][0])
        export['tree'] = tree
        f.write(json.dumps(export))
        f.close()

    def import_onClick(self):
        jobfile = QFileDialog.getOpenFileName(self, 'import', '', 'json file(*.json)')
        if isinstance(jobfile, tuple):
            jobfile = jobfile[0]
        if not jobfile:
            return
        f = open(jobfile, 'r')
        export = json.loads(f.read())
        for regex in export['match_regex']: self.app.match_regex_list.append(
            regex), self.app.match_regex_dialog.setupList()
        for regex in export['black_regex']: self.app.black_regex_list.append(
            regex), self.app.black_regex_dialog.setupList()
        for t in export['tree']:
            tid = t[0: t.index(' - ')]
            tname = t[t.index(' - ') + 3:]
            for item in export['tree'][t]:
                put_tree(self.app, tid, tname, item)


def put_tree(app, tid, tname, item):
    app.method_entry(tid, tname, item['clazz'], item['method'], item['args'])
    for child in item['child']:
        put_tree(app, tid, tname, child)
    app.method_exit(tid, item['retval'])


def gen_tree(item):
    if isinstance(item, TraceItem):
        res = {}
        res['clazz'] = item.clazz
        res['method'] = item.method
        res['args'] = item.args
        res['child'] = []
        for i in range(item.rowCount()):
            res['child'].append(gen_tree(item.child(i)))
        res['retval'] = item.retval
    elif isinstance(item, QStandardItem):
        res = []
        for i in range(item.rowCount()):
            res.append(gen_tree(item.child(i)))
    else:
        res = []
    return res


class ZenTracer:

    def __init__(self):
        global APP
        APP = self
        self.app = QApplication(sys.argv)
        self.ui = Ui_MainWindow()
        self.window = ZenTracerWindow(self)
        self.window.setWindowIcon(QIcon('icon.png'))
        self.ui.setupUi(self.window)
        self.setupAction()
        self.setupTreeModel()
        self.thread_map = {}
        self.black_regex_list = []
        self.match_regex_list = []
        self.black_regex_dialog = ListWindow(self.black_regex_list, "Black RegEx")
        self.match_regex_dialog = ListWindow(self.match_regex_list, "Match RegEx")
        self.window.show()
        threading.Timer(1, self.ui.logList.scrollToBottom).start()
        sys.exit(self.app.exec_())

    def setupAction(self):
        self.ui.actionAbout.triggered.connect(self.window.about_onClick)
        self.ui.actionBlack_Regex.triggered.connect(self.window.black_onClick)
        self.ui.actionMatch_Regex.triggered.connect(self.window.match_onClick)
        self.ui.actionStart.triggered.connect(self.window.start_onClick)
        self.ui.actionClean.triggered.connect(self.window.clean_onClick)
        self.ui.actionExportJSON.triggered.connect(self.window.export_onClick)
        self.ui.actionImportJSON.triggered.connect(self.window.import_onClick)

    def setupTreeModel(self):
        self.ui.logList.setModel(QStandardItemModel(self.ui.logList))
        self.ui.treeView.setModel(QStandardItemModel(self.ui.treeView))
        self.ui.treeView.model().setHorizontalHeaderLabels(['method', 'args', 'retval'])
        self.ui.treeView.setColumnWidth(0, 500)
        self.ui.treeView.setColumnWidth(1, 300)

    def method_entry(self, tid, tname, clazz, method, args):
        if tid not in self.thread_map:
            tItem = QStandardItem('{} - {}'.format(tid, tname))
            self.ui.treeView.model().appendRow(tItem)
            self.thread_map[tid] = {
                'current': tItem,
                'list': [tItem]
            }
        item = TraceItem(clazz, method, args, parent_item=self.thread_map[tid]['current'])
        self.thread_map[tid]['current'] = item
        self.thread_map[tid]['list'].append(item)

    def method_exit(self, tid, retval):
        self.thread_map[tid]['current'].set_retval(retval)
        self.thread_map[tid]['current'] = self.thread_map[tid]['current'].parent()

    def log(self, text):
        text = time.strftime('%Y-%m-%d %H:%M:%S:  [*] ', time.localtime(time.time())) + text
        self.ui.logList.model().insertRow(0, QStandardItem(text))
        # self.ui.logList.scrollToBottom()


if __name__ == '__main__':
    ZenTracer()
