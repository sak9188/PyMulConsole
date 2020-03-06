# -*- coding:UTF-8 -*-
import os
import Queue
import random
import subprocess
import sys
import time
from multiprocessing import Process
from multiprocessing.managers import BaseManager

# 发送任务的队列:
task_queue = Queue.Queue()
# 接收结果的队列:
result_queue = Queue.Queue()


def task_q():
    return task_queue
def result_q():
    return result_queue

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass

if __name__=='__main__':

    # 把两个Queue都注册到网络上, callable参数关联了Queue对象:
    QueueManager.register('get_task_queue', callable=task_q)
    QueueManager.register('get_result_queue', callable=result_q)
    # 绑定端口5000, 设置验证码'abc':
    manager = QueueManager(address=('127.0.0.1',5000),authkey=b'abc')
    # 启动Queue:
    manager.start()
    # 获得通过网络访问的Queue对象:
    task = manager.get_task_queue()
    result = manager.get_result_queue()
    # 放几个任务进去:
    for i in range(10):
        n = random.randint(0, 10000)
        print('Put task %d...' % n)
        task.put(n)

    software = 'python'
    path = os.getcwd()
    des_file = '\pr.py'
    sum_path = path + des_file
    # 暂时不管这个东西
    p = subprocess.Popen([software, sum_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)


    # 从result队列读取结果:
    print('Try get results...')
    for i in range(10):
        r = result.get(timeout=100)
        print('Result: %s' % r)
    # 关闭:
    manager.shutdown()
