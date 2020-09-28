"""对本地接口压力测试

    通过requests库访问本地接口
    判断随机返回的值概率是否与预期相同

"""


import requests
import json
import time

url = 'http://127.0.0.1:6565/lottery'

timeToRun = 10000  # 循环次数
prize_stuff = ['RTX3080', '三星980 pro', '猫头鹰D15S', '100元现金奖励', '200元代金券', '10000元余额宝体验基金']  # 奖励list，顺序无所谓
prize_num = [0] * len(prize_stuff)  # 创建一个和奖励list同样长度的list，初始化为0，用来记录每个奖励的次数


startTime = time.time()

for i in range(timeToRun):  # 循环请求该url
    res = requests.get(url, headers={'Connection': 'close'}, timeout=5)  # 需要设置headers为connection close，否则大量请求会直接失败
    res.encoding = 'utf-8'  # requests返回的结果需要编码，这里比较坑
    js = json.loads(res.text)  # 转json

    for j in range(len(prize_stuff)):  # 查找本次请求的返回值是奖励列表的哪一个，找到了就给prize_num同样位置的值+1
        if js['prize']['stuff'] == prize_stuff[j]:
            prize_num[j] += 1


for i in range(len(prize_stuff)):  # 后续的统计
    print(prize_stuff[i], end="")
    print("返回了", end="")
    print(prize_num[i], end="")
    print("次，概率为:", end="")
    Probability = round(prize_num[i] / timeToRun * 100, 3)  # round函数保留三位小数
    print(Probability, end="")
    print("%")

endTime = time.time()

print("请求共耗时")
print(endTime - startTime)
