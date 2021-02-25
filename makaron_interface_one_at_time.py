import traceback

import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor

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

time_to_Run = 50000  # 循环次数
success_num_requests = [0] * 1  # 成功次数
max_thread_num = 30  # 线程数
defeat_num_requests = [0] * 1  # 返回值非200的次数
avg_time_each_successful_request = [0] * 1  # 成功的请求耗时


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


def conn(response_code_is_200, response_code_not_200, request_time_if_successfully):
    whole_start_time = time.time()
    for i in range(len(url)):
        start_time = time.time()
        res = try_catch_conn(url[i], response_code_not_200)
        end_time = time.time()
        uri = url[i].split("?")[0]
        request_time = end_time - start_time  # 单次请求耗时
        print("单次url:" + uri + "请求耗时:" + str(request_time))
        res.encoding = 'utf-8'  # requests返回的结果需要编码，这里比较坑
        if str(res) == "<Response [200]>":
            response_code_is_200[0] += 1
            request_time_if_successfully[0] += request_time
            print("返回码为200次数:" + str(response_code_is_200[0]))
        else:
            response_code_not_200[0] += 1
            print("错误码：" + str(res))
        js = json.loads(res.text)  # 转json
        # print(js)
    whole_end_time = time.time()
    print("一次任务执行耗时:" + str(whole_end_time - whole_start_time))


if __name__ == '__main__':
    startTime = time.time()
    with ThreadPoolExecutor(max_workers=max_thread_num) as pool:  # 创建一个最大线程数为6的线程池，具体几个可以多试试
        for _ in range(time_to_Run):
        # while(True):
            # 将request提交给线程池
            pool.submit(conn, success_num_requests, defeat_num_requests, avg_time_each_successful_request)
    endTime = time.time()

    print("请求共耗时:" + str(endTime - startTime))
    print("平均耗时:" + str((avg_time_each_successful_request[0] / success_num_requests[0]) / len(url)))
    print("成功次数:" + str(success_num_requests[0]))
    print("失败次数:" + str(defeat_num_requests[0]))
