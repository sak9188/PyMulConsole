# -*- coding:UTF-8 -*-

import random
import time

import QueuePipe as pie

if __name__ == '__main__':
    # 绑定端口5000, 设置验证码'abc':
    manager = pie.GManager
    # 启动Queue:
    manager.start()
    # 获得通过网络访问的Queue对象:
    task = manager.get_server()
    result = manager.get_client()
    out = manager.get_client_out()
    # 放几个任务进去:
    for i in range(10):
        n = random.randint(0, 10000)
        print('Put task %d...' % n)
        task.put(n)
    # 从result队列读取结果:
    print('Try get results...')
    for i in range(10):
        r = result.get(timeout=100)
        print('Result: %s' % r)
        try:
            out = out.get(timeout=10)
            print out
        except:
            pass
    # 关闭:
    manager.shutdown()