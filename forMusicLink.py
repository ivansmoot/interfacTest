import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor

url = f"http://192.168.36.205:8100/musicLibrary/extract?url=%E8%AE%B8%E5%85%89%E6%B1%89%E3%80%8A%E5%88%AB%E5%86%8D%E6%83%B3%E8%A7%81%E6%88%91%E3%80%8B%20https%3A%2F%2Fc.y.qq.com%2Fbase%2Ffcgi-bin%2Fu%3F__%3DHnjcNCg%20%40QQ%E9%9F%B3%E4%B9%90"
timeToRun = 200000  # 循环次数
success_num = [0] * 1  # 成功次数


def conn(add_num):  # 把网络请求提出来放到一个方法里，参数为需要修改的list
    res = requests.get(url, headers={'Connection': 'close'}, timeout=5)  # 需要设置headers为connection close，否则大量请求会直接失败
    res.encoding = 'utf-8'  # requests返回的结果需要编码，这里比较坑
    js = json.loads(res.text)  # 转json
    if js['responseMsg'] == '成功':
        print("相等")
        add_num[0] += 1
    print(js)


if __name__ == '__main__':
    startTime = time.time()

    with ThreadPoolExecutor(max_workers=6) as pool:  # 创建一个最大线程数为6的线程池，具体几个可以多试试
        for _ in range(timeToRun):
            pool.submit(conn, success_num)  # 将request提交给线程池

    endTime = time.time()

    print("请求共耗时")
    print(endTime - startTime)
    print('成功次数')
    print(success_num[0])
