"""对本地接口压力测试

    通过requests库访问本地接口
    判断随机返回的值概率是否与预期相同

"""


import requests
import json
import time

url = 'http://127.0.0.1:6565/lottery'

timeToRun = 100000
prize_stuff = ['RTX3080', '三星980 pro', '猫头鹰D15S', '100元现金奖励', '200元代金券', '10000元余额宝体验基金']
prize_num = [0] * len(prize_stuff)


startTime = time.time()

for i in range(timeToRun):
    res = requests.get(url, headers={'Connection': 'close'})
    res.encoding = 'utf-8'
    js = json.loads(res.text)

    for j in range(len(prize_stuff)):
        if js['prize']['stuff'] == prize_stuff[j]:
            prize_num[j] += 1

endTime = time.time()


for i in range(len(prize_stuff)):
    print(prize_stuff[i], end="")
    print("返回了", end="")
    print(prize_num[i], end="")
    print("次，概率为:", end="")
    print((prize_num[i] / timeToRun) * 100, end="")
    print("%")

print("请求共耗时")
print(endTime - startTime)
