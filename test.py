import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor

url = f"https://appdev.api.versa-ai.com/menu/editing?appSource=web&appVersion=4.5.9&appkey=test&clientType=app&countryCode=CN&deviceId=8a1449de224a3cc0&imei=&lang=zh-cn&mobileType=SM-G9650&osType=ANDROID&osVersion=10&sign=47904D4FC34A1B0380AACC9B11A0BFF1&timestamp=1613804392458&uid=&userToken="
timeToRun = 10000  # 循环次数
success_num = [0] * 1  # 成功次数
max_thread_num = 100
success_num_revise = [0] * max_thread_num
default_num = [0] * 1


def conn(add_num, add_num2):  # 把网络请求提出来放到一个方法里，参数为需要修改的list
    start_time = time.time()
    try:
        res1 = requests.get(url, headers={'Connection': 'close'}, timeout=5)
    except requests.exceptions.ConnectionError:
        print("ConnectionError失败了")
    except requests.exceptions.HTTPError:
        print("HTTPError失败了")
    except requests.exceptions.ReadTimeout:
        print("ReadTimeout失败了")
    except requests.exceptions.RetryError:
        print("RetryError失败了")
    except requests.exceptions.StreamConsumedError:
        print("StreamConsumedError失败了")
    except Exception:
        print("Exception失败了")
    end_time = time.time()
    # 需要设置headers为connection close，否则大量请求会直接失败
    res1.encoding = 'utf-8'  # requests返回的结果需要编码，这里比较坑
    if str(res1) == "<Response [200]>":
        add_num[0] += 1
        print(add_num[0])
    else:
        add_num2[0] += 1
        print("错误码：" + str(res1))

    request_time = end_time - start_time
    if request_time >= 2:
        print("请求耗时大于2s，耗时" + str(request_time))
    js1 = json.loads(res1.text)  # 转json
    # print(js1)


if __name__ == '__main__':
    startTime = time.time()
    total_time = 0
    with ThreadPoolExecutor(max_workers=max_thread_num) as pool:  # 创建一个最大线程数为6的线程池，具体几个可以多试试
        for _ in range(timeToRun):
            total_time += 1
            pool.submit(conn, success_num, default_num)  # 将request提交给线程池

    endTime = time.time()

    print("请求共耗时")
    print(endTime - startTime)
    print("成功次数：" + str(success_num[0]))
    print("失败：" + str(default_num[0]))
    print("循环次数：" + str(total_time))
