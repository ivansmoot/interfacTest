"""

    搜狗语音转写接口压力测试
    分两个接口，第一个接口传参音频文件，拿到taskId
    第二个接口根据taskId，获取结果
    其中第二个接口需要持续等待，一直等到非空的返回
    第一个接口给的音频文件有两种，第一种为pcm文件，是需要的格式
    如果是m4a文件，则需要转成pcm的

"""

import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor

# url = f"http://192.168.36.205:8100/audio2subtitle/url?url=http%3A%2F%2Fversa-static.oss-cn-shanghai.aliyuncs.com%2F1m.pcm"
# url = f"http://192.168.36.205:8100/audio2subtitle/url?url=http://versa-static.oss-cn-shanghai.aliyuncs.com/tmp/recognizeVoiceCaptionAudio.m4a"
url = f"http://192.168.36.205:8100/audio2subtitle/url?url=https://static01.versa-ai.com/upload/047fb40cbcb2/d4367288-f163-4a29-8e42-149341641609.m4a"
timeToRun = 1000  # 循环次数
success_num = [0] * 1  # 成功次数


def conn(add_num):  # 把网络请求提出来放到一个方法里，参数为需要修改的list
    res1 = requests.post(url, headers={'Connection': 'close'}, timeout=50)  # 需要设置headers为connection close，否则大量请求会直接失败
    res1.encoding = 'utf-8'  # requests返回的结果需要编码，这里比较坑
    js1 = json.loads(res1.text)  # 转json
    if js1['responseMsg'] != '成功':
        print('请求1失败')
    taskId = js1['result']['taskId']
    url2 = f'http://192.168.36.205:8100/audio2subtitle?taskId={taskId}'
    print(js1)
    js2 = ""
    res = None
    # 第二个请求没返回，就一直请求
    while res is None or res == []:
        res2 = requests.get(url2, headers={'Connection': 'close'}, timeout=5)
        js2 = json.loads(res2.text)  # 转json
        res = js2['result']['result']
        time.sleep(1)
    print(js2)
    if js2['responseMsg'] == '成功':
        add_num[0] += 1
    else:
        print('请求2失败')


if __name__ == '__main__':
    startTime = time.time()

    with ThreadPoolExecutor(max_workers=30) as pool:  # 创建一个最大线程数为6的线程池，具体几个可以多试试
        for _ in range(timeToRun):
            pool.submit(conn, success_num)  # 将request提交给线程池

    endTime = time.time()

    print("请求共耗时")
    print(endTime - startTime)
    print('成功次数')
    print(success_num[0])
