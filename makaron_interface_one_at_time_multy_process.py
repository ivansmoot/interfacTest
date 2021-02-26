from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import os
import time
import threading
import traceback
import requests
import json
import urllib.parse
"""

    逐步增大接口压测的线程数: 如开始是10个线程，每隔十分钟加10个线程
    方式：每十分钟加1个进程，每个进程起10个线程
    每个进程的任务数要相应减少
    每个进程的数据单独统计

"""

url = []
url.append(f"https://vmk-dev.api.versa-ai.com//basic/material/app/queryBasicInfo?appSource=appstore&appVersion=1.3.0"
           f"&appkey=vmkndev-ios&clientType=app&countryCode=&deviceId=d2e475d4862f623230aa98467ecd2146"
           f"&idfa=00000000-0000-0000-0000-000000000000&lang=&mnet=&mobileType=iPhone13%2C3&mobileTypeCode=iPhone13%2C3"
           f"&osType=iOS&osVersion=14.1&pointx=&pointy=&sign=9C7EE9043DBEA9364FF98F915E8F1D0F&timestamp=1614136197031")
url.append(f"https://vmk-dev.api.versa-ai.com/guoman/material/app/titleList?appSource=appstore&appVersion=1.3.0"
           f"&appkey=vmkndev-ios&clientType=app&countryCode=&deviceId=d2e475d4862f623230aa98467ecd2146"
           f"&idfa=00000000-0000-0000-0000-000000000000&lang=&mnet=&mobileType=iPhone13%2C3&mobileTypeCode=iPhone13%2C3"
           f"&osType=iOS&osVersion=14.1&pointx=&pointy=&sign=28831D292AD471A0DDF315DA165E6A1D&timestamp=1614136197032")
url.append(f"https://vmk-dev.api.versa-ai.com//guoman/material/app/concurrentQueryInfo?appSource=appstore"
           f"&appVersion=1.3.0&appkey=vmkndev-ios&clientType=app&countryCode=&deviceId=d2e475d4862f623230aa98467ecd2146"
           f"&idfa=00000000-0000-0000-0000-000000000000&lang=&mnet=&mobileType=iPhone13%2C3&mobileTypeCode=iPhone13%2C3"
           f"&osType=iOS&osVersion=14.1&pointx=&pointy=&sign=79D239ECA449600D4E08606D4A61112B&timestamp=1614136197317"
           f"&titleCode=3be420c9b02445e7b2c781461cd71302")
url.append(f"https://appdev.api.versa-ai.com/menu/editing?appSource=web&appVersion=4.5.9&appkey=test&clientType=app"
           f"&countryCode=CN&deviceId=8a1449de224a3cc0&imei=&lang=zh-cn&mobileType=SM-G9650&osType=ANDROID&osVersion=10"
           f"&sign=47904D4FC34A1B0380AACC9B11A0BFF1&timestamp=1613804392458&uid=&userToken=")
url.append(f"https://appdev.api.versa-ai.com/launch/ads?appSource=web&appVersion=5.0.0&appkey=test"
           f"&clientType=app&countryCode=CN&deviceId=182b77e08b8dbcff&imei=&lang=zh-cn&mobileType=OPPO_R11s"
           f"&osType=ANDROID&osVersion=8.1.0&sign=02C59B1340B4E37270D9451A846FB634&timestamp=1613976889862&uid="
           f"&userToken=")
url.append(f"https://appdev.api.versa-ai.com/template?appSource=web&appVersion=5.0.0&appkey=test&clientType=app"
           f"&countryCode=CN&deviceId=182b77e08b8dbcff&imei=&lang=zh-cn&mobileType=OPPO_R11s"
           f"&osType=ANDROID&osVersion=8.1.0&sign=8974BC8E68CDF3AC38C1DA5460909940&timestamp=1613976891893"
           f"&uid=&userToken=")
url.append(f"https://appdev.api.versa-ai.com/sticker?appSource=web&appVersion=5.0.0&appkey=test&clientType=app"
           f"&countryCode=CN&deviceId=182b77e08b8dbcff&imei=&lang=zh-cn&mobileType=OPPO_R11s&osType=ANDROID"
           f"&osVersion=8.1.0&sign=36D94941FDB145D140435AA1FC30272D&timestamp=1614151683488&uid=&userToken=")
url.append(f"https://appdev.api.versa-ai.com/community/feed/recommend/templates?action=down"
           f"&appSource=web&appVersion=4.5.9&appkey=test&clientType=app&countryCode=CN&deviceId=8a1449de224a3cc0&from=1"
           f"&imei=&lang=zh-cn&mobileType=SM-G9650&osType=ANDROID&osVersion=10&sign=C677DE2D534BE2466251E3364599BB20"
           f"&tabId=459061311793057793&timestamp=1614233868270&uid=&userToken=")

time_to_Run = 5  # 每个线程的循环次数
max_process_num = 3  # 进程数
sleep_time_during_create_process = 1  # 每两次创建进程的间隔时间
max_thread_num = 3  # 每个进程的线程数


# 每次请求函数,传入要请求的url和一个用来统计返回码非200次数的值,返回这次请求的返回值,或抛出异常
def try_catch_conn(uri, code_not_200):
    response = ""
    try:
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        # 需要设置headers为connection close，否则大量请求会直接失败
        response = requests.get(uri, headers={'Connection': 'close'}, timeout=(5, 5))
        print(response.elapsed)
    except requests.exceptions.ConnectionError:
        code_not_200[0] += 1
        traceback.print_exc()
        print("ConnectionError失败了")
    except requests.exceptions.HTTPError:
        code_not_200[0] += 1
        traceback.print_exc()
        print("HTTPError失败了")
    except requests.exceptions.ReadTimeout:
        code_not_200[0] += 1
        traceback.print_exc()
        print("ReadTimeout失败了")
    except requests.exceptions.RetryError:
        code_not_200[0] += 1
        traceback.print_exc()
        print("RetryError失败了")
    except requests.exceptions.StreamConsumedError:
        code_not_200[0] += 1
        traceback.print_exc()
        print("StreamConsumedError失败了")
    except Exception:
        code_not_200[0] += 1
        traceback.print_exc()
        print("Exception失败了")
    finally:
        requests.session().close()
    return response


# 任务函数，每个线程都应该去调用此函数
def conn(response_code_is_200, response_code_not_200, request_time_if_successfully):
    # 拿到线程号
    thread_num = str(threading.current_thread().name)
    # 处理一下线程号
    thread_num_str = "[线程" + thread_num + "]"
    whole_start_time = time.time()
    for j in range(len(url)):
        start_time = time.time()
        res = try_catch_conn(url[j], response_code_not_200)
        end_time = time.time()
        # 拿到这次请求url的地址
        uri = str(urllib.parse.urlsplit(url[j]).path)
        request_time = end_time - start_time  # 单次请求耗时
        print(thread_num_str + "单次url:" + uri + "请求耗时:" + str(request_time))
        res.encoding = 'utf-8'  # requests返回的结果需要编码，这里比较坑
        if str(res) == "<Response [200]>":
            response_code_is_200[0] += 1
            request_time_if_successfully[0] += request_time
            print(thread_num_str + "返回码为200次数:" + str(response_code_is_200[0]))
        else:
            response_code_not_200[0] += 1
            print(thread_num_str + "错误码：" + str(res))
        js = json.loads(res.text)  # 转json
        # print(js)
    whole_end_time = time.time()
    print(thread_num_str + "一次任务执行耗时:" + str(whole_end_time - whole_start_time))


def multiple_threading_task():
    # 每个进程使用自己的变量
    success_num_requests = [0] * 1  # 成功次数
    defeat_num_requests = [0] * 1  # 返回值非200的次数
    avg_time_each_successful_request = [0] * 1  # 成功的请求耗时

    # 拿到进程号
    process_num = os.getpid()
    # 处理进程号
    process_num_str = "[进程" + str(process_num) + "]"

    print(process_num_str + "正在创建线程池...")
    with ThreadPoolExecutor(max_workers=max_thread_num) as thread_pool:  # 创建一个最大线程数为6的线程池，具体几个可以多试试
        for _ in range(time_to_Run):
            # 将request提交给线程池
            thread_pool.submit(conn, success_num_requests, defeat_num_requests, avg_time_each_successful_request)
    print(process_num_str + "执行完毕...")
    print(process_num_str + "成功次数: " + str(success_num_requests[0]))
    print(process_num_str + "接口返回值非200次数: " + str(defeat_num_requests[0]))
    print(process_num_str + "成功的请求总耗时: " + str(avg_time_each_successful_request[0]))


if __name__ == '__main__':
    pool = Pool(processes=max_process_num)
    for i in range(max_process_num):
        print("准备创建第" + str(i) + "个进程")
        pool.apply_async(multiple_threading_task)
        print("进程创建完毕，等待下一次创建进程")
        time.sleep(sleep_time_during_create_process)
    pool.close()
    pool.join()
