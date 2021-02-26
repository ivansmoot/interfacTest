from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Lock, Pool
import os
import time
import threading


def conn(url):
    print("线程号: " + str(threading.current_thread().name))
    print("进程号: " + str(os.getpid()))
    print("正在请求url:" + url)


def get_multiple_thread(url):
    print("pid: " + str(os.getpid()))
    with ThreadPoolExecutor(max_workers=3) as pool:
        for _ in range(10):
            time.sleep(1)
            pool.submit(conn, (url,))


if __name__ == '__main__':
    # process1 = Process(target=get_multiple_thread, args=('url1',))
    # process1.start()
    # process1.join()
    #
    # print('等待中...')
    # time.sleep(2)
    #
    # process2 = Process(target=get_multiple_thread, args=('url2',))
    # process2.start()
    # process2.join()
    pool = Pool(processes=2)
    pool.apply_async(get_multiple_thread, ('url1',))
    time.sleep(2)
    print('等待中...')
    pool.apply_async(get_multiple_thread, ('url2',))
    pool.close()
    pool.join()
