"""对本地接口压力测试

    通过requests库访问本地接口
    判断随机返回的值概率是否与预期相同

"""


import requests
import json
import time
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor


url = 'http://127.0.0.1:6565/lottery'

timeToRun = 10000
prize_stuff = ['RTX3080', '三星980 pro', '猫头鹰D15S', '100元现金奖励', '200元代金券', '10000元余额宝体验基金']
prize_num = [0] * len(prize_stuff)


def conn(add_prize):
    res = requests.get(url, headers={'Connection': 'close'}, timeout=5)
    res.encoding = 'utf-8'
    js = json.loads(res.text)
    for j in range(len(prize_stuff)):
        if js['prize']['stuff'] == prize_stuff[j]:
            add_prize[j] += 1


if __name__ == '__main__':
    startTime = time.time()
    # for i in range(timeToRun):
    #     conn()
    # pool = Pool()
    # for i in range(timeToRun):
    #     pool.apply_async(conn, (prize_num,))
    # pool.close()
    # pool.join()
    with ThreadPoolExecutor(max_workers=6) as pool:
        for i in range(timeToRun):
            pool.submit(conn, prize_num)
    for i in range(len(prize_stuff)):
        print(prize_stuff[i], end="")
        print("返回了", end="")
        print(prize_num[i], end="")
        print("次，概率为:", end="")
        Probability = round(prize_num[i] / timeToRun * 100, 3)
        print(Probability, end="")
        print("%")
    endTime = time.time()
    print("请求共耗时")
    print(endTime - startTime)
