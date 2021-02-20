import threading
import requests

url = f"https://appdev.api.versa-ai.com/menu/editing" \
      f"?appSource=web&appVersion=4.5.9&appkey=test&clientType=app&countryCode=CN&deviceId=8a1449de224a3cc0" \
      f"&imei=&lang=zh-cn&mobileType=SM-G9650&osType=ANDROID&osVersion=10&sign=47904D4FC34A1B0380AACC9B11A0BFF1" \
      f"&timestamp=1613804392458&uid=&userToken="

threads = []
thread_num = 10


class Thread(threading.Thread):
    def __init__(self, threadName):
        threading.Thread.__init__(self, name='thread' + threadName)

    def run(self):
        res1 = requests.get(url, headers={'Connection': 'close'}, timeout=5)
        res1.encoding = 'utf-8'
        print(res1.text)


if __name__ == '__main__':
    for i in range(thread_num):
        threads.append(Thread(str(i)))

    for j in threads:
        j.start()

    for k in threads:
        k.join()
