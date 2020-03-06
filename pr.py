# -*- coding:UTF-8 -*-

import Queue
import sys
import time
import QueueBranch as branc

m = branc.GetServanter()
m.connect()
 
# server = m.get_server()
# client = m.get_client()

class myout():
    out = m.get_client_out()

    @classmethod
    def write(cls, s):
        try:
            cls.out.put(s.replace('\r\n',"").replace('\n',""))
        except IOError:
            sys.exit(0)

sys.stdout = myout

while True:
    print 'try to get me123'
    time.sleep(2)
