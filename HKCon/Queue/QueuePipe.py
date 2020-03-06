# -*- coding:UTF-8 -*-

import sys, time, Queue
import QueueBase
from multiprocessing.managers import BaseManager

GManager = None
GAuthkey = b'hk'
GAddres = '127.0.0.1'
GPort = 9188

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    reg_func = {}
    pass


def reg_func_queue():
    import sys
    mod = sys.modules[__name__]
    for item in dir(mod):
        if item.startswith('get_'):
            func = getattr(mod, item)
            QueueManager.register(func.__name__, callable=func)

def get_server():
    return QueueBase.GQuedict.get_queue(sys._getframe().f_code.co_name)


def get_client():
    return QueueBase.GQuedict.get_queue(sys._getframe().f_code.co_name)


def get_client_out():
    return QueueBase.GQuedict.get_queue(sys._getframe().f_code.co_name)

reg_func_queue()

GManager = QueueManager(address=(GAddres,GPort),authkey=GAuthkey)

