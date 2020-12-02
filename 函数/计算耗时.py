import time


# start = time.time()
# time.sleep(10)
# end = time.time()
# print("运行这段代码耗时{}秒".format(end - start))

def cal_time(func):
    start = time.time()
    func()
    end = time.time()
    print("运行这段代码耗时{}秒".format(end - start))


def demo():
    x = 1
    for i in range(1, 100000000):
        x += i
    print(x)


cal_time(demo)
