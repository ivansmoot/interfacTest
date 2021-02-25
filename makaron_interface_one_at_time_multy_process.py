import multiprocessing
import os
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor


# TODO
# 进程通信，每个进程写入自己的变量，最后累加变量
# conn里进行循环，循环次数为总次数/进程数
# 一些耗时的计算

url = f"https://appdev.api.versa-ai.com/menu/editing?appSource=web&appVersion=4.5.9&appkey=test&clientType=app" \
      f"&countryCode=CN&deviceId=8a1449de224a3cc0&imei=&lang=zh-cn&mobileType=SM-G9650&osType=ANDROID&osVersion=10" \
      f"&sign=47904D4FC34A1B0380AACC9B11A0BFF1&timestamp=1613804392458&uid=&userToken="

time_to_Run = 10000  # 循环次数
success_num_requests = [0] * 1  # 成功次数
max_thread_num = 200  # 线程数
defeat_num_requests = [0] * 1  # 返回值非200的次数
avg_time_each_successful_request = [0] * 1  # 成功的请求耗时
processes_num = 10  # 进程数


# 定义一个函数，准备作为新进程的 target 参数
def try_catch_conn(uri, code_not_200):
    response = ""
    this_pid = str(os.getpid())
    try:
        # 需要设置headers为connection close，否则大量请求会直接失败
        response = requests.get(uri, headers={'Connection': 'close'}, timeout=5)
    except requests.exceptions.ConnectionError:
        code_not_200[0] += 1
        print("[" + this_pid + "]ConnectionError失败了")
    except requests.exceptions.HTTPError:
        code_not_200[0] += 1
        print("[" + this_pid + "]HTTPError失败了")
    except requests.exceptions.ReadTimeout:
        code_not_200[0] += 1
        print("[" + this_pid + "]ReadTimeout失败了")
    except requests.exceptions.RetryError:
        code_not_200[0] += 1
        print("[" + this_pid + "]RetryError失败了")
    except requests.exceptions.StreamConsumedError:
        code_not_200[0] += 1
        print("[" + this_pid + "]StreamConsumedError失败了")
    except Exception:
        code_not_200[0] += 1
        print("[" + this_pid + "]Exception失败了")
    return response


def conn(response_code_is_200, response_code_not_200, request_time_if_successfully):
    for _ in range(int(time_to_Run / processes_num)):
        this_pid = str(os.getpid())
        # res = ""  # 保存请求结果
        start_time = time.time()
        res = try_catch_conn(url, response_code_not_200)
        end_time = time.time()
        request_time = end_time - start_time  # 单次请求耗时
        res.encoding = 'utf-8'  # requests返回的结果需要编码，这里比较坑
        if str(res) == "<Response [200]>":
            response_code_is_200[0] += 1
            request_time_if_successfully[0] += request_time
            print("[" + this_pid + "]返回码为200次数:" + str(response_code_is_200[0]))
        else:
            response_code_not_200[0] += 1
            print("[" + this_pid + "]错误码：" + str(res))


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    for i in range(6):
        pool.apply_async(conn, (success_num_requests, defeat_num_requests, avg_time_each_successful_request))
    pool.close()
    pool.join()
