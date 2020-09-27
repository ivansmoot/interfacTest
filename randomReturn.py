"""随机返回一个值

    该方法接受一个dict，eg:
    example = {
        '返回值1': 10,
        '返回值2': '20',
        '返回值3': 20,
        '返回值4': 50
    }
    key为可能的返回值，value为对应返回值的概率，概率为string或number均可，概率和需要为100

"""

import random
import unicodedata


def get_randomKey(formatDict: dict):
    sum_of_probabilities = 0  # 校验给定的概率和是否等于100
    list_of_probabilities = []  # 把概率放在一个list里
    list_of_return = []  # 把需要返回的值放在一个list里
    for key, value in formatDict.items():  # 遍历该dict
        if is_number(value):  # 判断概率是否都能转成数字
            sum_of_probabilities += float(value)  # 概率求和
            list_of_probabilities.append(float(value))
            list_of_return.append(key)
        else:
            return TypeError  # 如果概率不是数字就返回错误
    if sum_of_probabilities != 100:
        return ValueError  # 如果概率和不是100也返回错误
    back_of_probabilities = []
    back_of_probabilities.extend(list_of_probabilities)  # 备份一下概率list，因为等下要求和，求完了之前的值就没了
    for i in range(len(list_of_probabilities)):  # 每个概率要加上前面所有概率，如10，20，20，50，会变成10，30，50，100
        sum_of_left_all = 0
        for j in range(i + 1):
            sum_of_left_all += back_of_probabilities[j]  # 把左边的都加上
        list_of_probabilities[i] = sum_of_left_all  # 再重新赋值

    # 确定随机返回的是哪个值
    random_number = random.randint(1, 10000)
    random_number = float(random_number / 100)  # 产生一个随机数
    list_of_probabilities.append(random_number)
    list_of_probabilities.sort()  # 把这个随机数加入数组并排序，让这个数找到合适的位置
    return list_of_return[list_of_probabilities.index(random_number)]  # 确定返回值


def is_number(s):  # 判断是否是数字
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


# dp = {
#     '奖励1': '5',
#     '奖励3': '30',
#     '奖励2': 10,
#     '奖励5': '5',
#     '奖励4': 50
# }

# get_randomKey(dp)

# if __name__ == '__main__':
#     time = 10000
#     num_of_stuff1 = 0
#     num_of_stuff2 = 0
#     num_of_stuff3 = 0
#     num_of_stuff4 = 0
#     num_of_stuff5 = 0
#
#     for i in range(time):
#         stuff = get_randomKey(dp)
#         if stuff == '奖励1':
#             num_of_stuff1 += 1
#         elif stuff == '奖励2':
#             num_of_stuff2 += 1
#         elif stuff == '奖励3':
#             num_of_stuff3 += 1
#         elif stuff == '奖励4':
#             num_of_stuff4 += 1
#         elif stuff == '奖励5':
#             num_of_stuff5 += 1
#
#     print(num_of_stuff1 / time)
#     print(num_of_stuff2 / time)
#     print(num_of_stuff3 / time)
#     print(num_of_stuff4 / time)
#     print(num_of_stuff5 / time)
