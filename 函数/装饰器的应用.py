def canplay(func):
    def inner(x, y, *args, **kwargs):
        clock = kwargs.get('clock')
        #        print(clock, type(clock))
        if clock is None:
            print('请告诉我现在几点了')
        elif clock < 6 or clock >= 22:
            print('注意休息！')
        else:
            func(x, y)

    return inner


@canplay
def playgame(name, game):
    print("{}正在玩{}".format(name, game))


playgame('张三', '王者荣耀 ', clock=7)
