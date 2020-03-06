# -*- coding:UTF-8 -*-
import os
import sys
import subprocess

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QPalette, QTextCursor
from PyQt5.QtWidgets import *

from HKCon.Queue import QueuePipe
from HKCon.ThreadPool import Thread
from Thread import ThreadInterval

m = QueuePipe.GManager
out = None

class MonitorWindow(QMainWindow):
    def __init__(self, title):
        super(QWidget, self).__init__()
        self.p_dict = {}

        self.setWindowTitle(title)
        self.init()


    def init(self):
        widget = QWidget()
        self.setCentralWidget(widget) 

        # 添加一部分面板
        panel1Btn = QPushButton(u"面板1")
        panel2Btn = QPushButton(u"面板2")
        panel3Btn = QPushButton(u"面板3")
        panel4Btn = QPushButton(u"面板4")
        panel5Btn = QPushButton(u"面板5")
 
        vbox = QVBoxLayout()
        vbox.addWidget(panel1Btn)
        vbox.addWidget(panel2Btn)
        vbox.addWidget(panel3Btn)
        vbox.addWidget(panel4Btn)
        vbox.addWidget(panel5Btn)

        tab1 = QTabWidget()
        scroll = QScrollArea()
        self.tbox = tbox = MonitorTerminal()
        menubar = self.menuBar()
        file = menubar.addMenu("文件")
        action = file.addAction("退出")
        action.triggered.connect(self.processtrigger)
        file.addSeparator()


        tbox = MonitorTerminal()
        tbox.setBackgroundColor(QColor(0,0,0))
        tbox.append_cn_str("终端1")


        software = 'python'
        path = os.getcwd()
        des_file = '\pr.py'
        sum_path = path + des_file
        p = subprocess.Popen([software, sum_path])
        self.p_dict["terminal1"] = p
        tbox.start_t()

        scroll.setWidget(tbox)
        scroll.setWidgetResizable(True)
        tab1.addTab(scroll, u"终端1")
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addWidget(tab1)
        
        widget.setLayout(hbox)       
        self.setGeometry(0, 0, 800, 600) 
        self.center()
        self.show()

    def processtrigger(self, qaction):
        print(qaction.text()+" is triggered!")

    def center(self):
        """ 控制窗口显示在屏幕中心的方法 """
        #获得窗口
        qr = self.frameGeometry()
        #获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        #显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def terminal_p(self):
        m.shutdown()
        for val in self.p_dict.itervalues():
            if val:
                print "kill pid:", val.pid
                val.kill()

    def closeEvent(self, event):
        self.terminal_p()
        os._exit(0) 


def append_str(func):
    def wrapper(self, s, c=None, si=None):
        func(self, s, c, si)
        # 恢复默认
        self.setFontFamily(self.font)
        self.setTextColor(self.color)
        self.setFontPointSize(self.size)
    return wrapper


class MonitorTerminal(QTextEdit):
    def __init__(self, str='', font='Consolas', color=QColor(250,250,250), size=13, QWidgetparent=None):
        super(MonitorTerminal, self).__init__(str, QWidgetparent)
        self.setReadOnly(True)
        self.font = font
        self.color = color
        self.size = size
        
        self.max_length = 1200
        self._thread = None
        self.__length = 0

    def setBackgroundColor(self, qcolor):
        palette = QPalette()
        palette.setColor(QPalette.Base, qcolor)
        self.setPalette(palette)

    @append_str
    def append_cn_str(self, s, qcolor=None, size=None):
        self.setFontFamily('FZSuXinShiLiuKai-R-JF')
        self.setTextColor(self.color)
        self.setFontPointSize(self.size)
        if qcolor:
            self.setTextColor(qcolor)
        if size:
            self.setFontPointSize(size)
        self.append(s)

    def append(self, s):
        super(MonitorTerminal, self).append(s)
        if self.__length == self.max_length:
            self.remove_top_line()
            return
        self.__length += 1

    def write(self, s):
        self.append(s)

    def remove_top_line(self):
        txtcur = self.textCursor()
        txtcur.setPosition(0)
        txtcur.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
        txtcur.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor)
        txtcur.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        txtcur.removeSelectedText()

    def start_t(self):
        if not self._thread:
            self._thread = ThreadInterval(self.__readio, 0.1)
            self._thread.start()
            self._thread.signal.connect(self.write)

    def slot_thread_txt(self, s):
        self.write(s)

    def __readio(self):
        try:
            s = out.get(timeout=1)
        except Exception:
            s = None
        return s      

    def terminate(self):
        print self.font
        print self.size
        

if __name__ == '__main__':
    m.start()
    app = QApplication(sys.argv)
    out = m.get_client_out()
    win = MonitorWindow(u'多进程终端监视器')

    sys.exit(app.exec_())

# QObject::connect: Cannot queue arguments of type 'QTextBlock'
# (Make sure 'QTextBlock' is registered using qRegisterMetaType().)
# QObject::connect: Cannot queue arguments of type 'QTextCursor'
# (Make sure 'QTextCursor' is registered using qRegisterMetaType().)
