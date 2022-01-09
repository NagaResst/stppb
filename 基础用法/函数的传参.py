def say_hello(name, age, city='百京'):
    print("大家好，我是{}，我今年{}，我来自{}".format(name, age, city))


say_hello('jack', age=19)


def get_sum(x):
    # def get_sum(x,*args,**kwargs)
    fsum = 0
    for s in x:
        fsum += s
    return fsum


nums = []
while True:
    userIn = int(input('请输入想要求和的数字,输入0结束'))
    nums.append(userIn)
    if userIn == 0:
        break
print(get_sum(nums))
