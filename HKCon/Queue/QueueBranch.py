# -*- coding:UTF-8 -*-

from multiprocessing.managers import BaseManager

import QueuePipe as pie


class ServManager(BaseManager):
    pass

def reg_all_function():
    for fvar in dir(pie):
        if fvar.startswith('get_'):
            ServManager.register(fvar)

def GetServanter():
    return ServManager(address=(pie.GAddres,pie.GPort),authkey=pie.GAuthkey)

reg_all_function()
