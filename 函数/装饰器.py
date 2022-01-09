import time


def cal_time(func):
    def inner():
        start = time.time()
        s = func()
        end = time.time()
        print("运行这段代码耗时{}秒".format(end - start))
        return s

    return inner


@cal_time
def demo():
    x = 1
    for i in range(1, 100000000):
        x += i
    return x


print(demo())

