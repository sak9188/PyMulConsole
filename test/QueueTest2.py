import sys, time, Queue

import QueueBranch as branc
 
m = branc.GetServanter()
m.connect()
 
task = m.get_server()
result = m.get_client()
 
for i in range(10):
    try:
        n = task.get(timeout = 1)
        print('run task %d * %d' % (n, n))
        r = '%d * %d = %d' % (n, n, n*n)
        time.sleep(1)
        result.put(r)
    except Queue.Empty:
        print('task queque is empty')
 
print('worker exit')