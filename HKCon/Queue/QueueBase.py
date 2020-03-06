# -*- coding:UTF-8 -*-

import Queue

class QueueDict():
    def __init__(self):
        self.que_dict = {}

    def get_queue(self, name):
        q = self.que_dict.get(name)
        if q:
            return q
        else:
            self.que_dict[name] = Queue.Queue()
            return self.que_dict[name]

GQuedict = QueueDict()