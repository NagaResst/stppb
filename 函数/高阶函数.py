def test():
    print("我是test函数")
    return 'hello'


def demo():
    print("我是demo函数")
    return test


def bar():
    print("我是bar函数")
    return test()


x = demo()  # return test 返回了一个函数  test并未执行
print('结果X', x)

y = x()  # 返回了一个值    因为x() 把前面返回的函数执行了
print('结果Y', y)

z = bar()  # return test() 返回的时候执行了函数 所以返回的是值
print('结果Z', z)
