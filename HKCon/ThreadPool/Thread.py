# -*- coding:UTF-8 -*-

import time
import threading
from PyQt5.QtCore import QThread, pyqtSignal


class ThreadInterval(QThread):
    signal = pyqtSignal(str) 
    def __init__(self, callback, interval):
        '''
        :param callback:  callback function to invoke
        :param interval: time in seconds after which are required to fire the callback
        :type callback: function
        :type interval: int
        '''
        self.callback = callback
        self.event = threading.Event()
        self.interval = interval
        super(ThreadInterval, self).__init__()

    def run(self):
        while not self.event.wait(self.interval):
            s = self.callback()
            if s:
                self.signal.emit(s)

    def cancel(self):
        self.event.set()

    def start(self, time=None):
        if time:
            self.set_lifetime(time)
        super(ThreadInterval, self).start()

    def set_lifetime(self, time):
        threading.Timer(time, self.cancel).start()
