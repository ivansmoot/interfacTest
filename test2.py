import threading_request
import time


class thread(threading_request.Thread):
    def __init__(self, threadname):
        threading_request.Thread.__init__(self, name='线程' + threadname)

    def run(self):
        print('%s:Now timestamp is %s'%(self.name,time.time()))


threads = []
for a in range(int(5)):  # 线程个数
    threads.append(thread(str(a)))
for t in threads:  # 开启线程
    t.start()
for t in threads:  # 阻塞线程
    t.join()
print('END')
