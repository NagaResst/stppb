import time


def cal_time(func):
    def inner():
        start = time.time()
        func()
        end = time.time()
        print("运行这段代码耗时{}秒".format(end - start))

    return inner


@cal_time
def demo():
    x = 1
    for i in range(1, 100000000):
        x += i
    print(x)


demo()
