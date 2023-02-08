#! /usr/bin/python3
def func(x, *args, **kwargs):
    print('拿到参数x', x)
    print('拿到元组参数', args, type(args))
    print('拿到字典参数', kwargs, type(kwargs))


func('spring', 3, 4, 6, 3, 2, word='hello', count=1, second='world')
