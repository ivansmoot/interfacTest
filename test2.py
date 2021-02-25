url = []
url.append(f"https://appdev.api.versa-ai.com/menu/editing?appSource=web&appVersion=4.5.9&appkey=test&clientType=app"
           f"&countryCode=CN&deviceId=8a1449de224a3cc0&imei=&lang=zh-cn&mobileType=SM-G9650&osType=ANDROID&osVersion=10"
           f"&sign=47904D4FC34A1B0380AACC9B11A0BFF1&timestamp=1613804392458&uid=&userToken=")

uri = url[0].split("/")[3]
print(uri)
