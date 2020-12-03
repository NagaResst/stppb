def outer():
    print("这是外部函数")

    def inner():
        print("这是内部函数")

    return inner


outer()
outer()()
