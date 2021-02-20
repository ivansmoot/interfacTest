a1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
target1 = 10


def judge(target, a):
    for b in a:
        if target in b:
            return True
    return False


if judge(target1, a1):
    print('在里面')
else:
    print('不在里面')

