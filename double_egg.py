import requests
import json
from concurrent.futures import ThreadPoolExecutor


url = f"http://192.168.36.205:5000/api/vmanage/list/put?"
timeToRun = 50
success_num = [0] * timeToRun  # 隐藏款次数
fail_num = [0] * timeToRun  # 未中奖次数
defeat_num = [0] * timeToRun  # 请求失败次数
num_05 = 0  # 未中奖
num_14 = 0  # 中了一次
num_23 = 0  # 中了两次
num_32 = 0  # 中了三次
num_41 = 0  # 中了四次
num_50 = 0  # 中了五次


def conn(suc_num, fa_nul, de_num, num):
    for _ in range(4):
        res1 = requests.get(url, headers={'Connection': 'close'}, timeout=10)  # 需要设置headers为connection close，否则大量请求会直接失败
        res1.encoding = 'utf-8'  # requests返回的结果需要编码，这里比较坑
        js1 = json.loads(res1.text)  # 转json
        print('一次请求:')
        if js1 is not None:
            if 'responseMsg' in js1:
                if js1['responseMsg'] == '成功':
                    if 'result' in js1:
                        suc_num[num] += 1
                        print('隐藏款')
                    else:
                        fa_nul[num] += 1
                        print('未中奖')
                else:
                    de_num[num] += 1
                    print('请求失败')
            else:
                de_num[num] += 1
                print('请求失败')
        else:
            de_num[num] += 1
            print('请求失败')


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=5) as pool:  # 创建一个最大线程数为6的线程池，具体几个可以多试试
        for i in range(timeToRun):
            pool.submit(conn, success_num, fail_num, defeat_num, i)  # 将request提交给线程池
    for i in range(timeToRun):
        print('第' + str(i) + '个用户')
        print('隐藏款个数:')
        print(success_num[i])
        print('未中奖次数:')
        print(fail_num[i])
        print('请求失败次数:')
        print(defeat_num[i])
        if success_num[i] == 0:
            num_05 += 1
        elif success_num[i] == 1:
            num_14 += 1
        elif success_num[i] == 2:
            num_23 += 1
        elif success_num[i] == 3:
            num_32 += 1
        elif success_num[i] == 4:
            num_41 += 1
        elif success_num[i] == 5:
            num_50 += 1

    print('未中奖的人数')
    print(num_05)
    print('中奖一次的人数')
    print(num_14)
    print('中奖两次的人数')
    print(num_23)
    print('中奖三次的人数')
    print(num_32)
    print('中奖四次的人数')
    print(num_41)
    print('中奖五次的人数')
    print(num_50)



# if __name__ == '__main__':
#     for _ in range(timeToRun):
#         res1 = requests.get(url, headers={'Connection': 'close'}, timeout=5)  # 需要设置headers为connection close，否则大量请求会直接失败
#         res1.encoding = 'utf-8'  # requests返回的结果需要编码，这里比较坑
#         js1 = json.loads(res1.text)  # 转json
#         print(js1)
#         if js1['success'] == '成功':
#             if js1['result']:
#                 success_num[0] += 1
#                 print('隐藏款')
#             else:
#                 print('未中奖')
#         else:
#             print('请求失败')
