# -*- coding:UTF-8 -*-

import QueueBase

class A():
    def __init__(self):
        self.dict_func = {}

    def register(self, name, callable=None):
        self.dict_func[name] = callable

    def get(self, obj):
        return self.dict_func[obj]

QueueManager = A()

def QueueRegister(func):
    def wrapper():
        func(func.__name__)
        print func.__name__, func
        QueueManager.register(func.__name__, callable=func)
    return wrapper

@QueueRegister
def get_server(name=None):
    return QueueBase.GQuedict.get_queue(name)

@QueueRegister
def get_client(name=None):
    return QueueBase.GQuedict.get_queue(name)


get_server()
get_client()
print "A['get_server']", QueueManager.get('get_server')
print "finished"