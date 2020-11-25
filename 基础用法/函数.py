# def printNum():
#     print('1')
#     print('2')
#     print('3')
#     print('4')
#     print('5')
#
#
# num = int(input('请输入数字'))
# if 0 <= num <= 10:
#     printNum()
# elif 10 < num <= 20:
#     printNum()
#     printNum()
# else:
#     for i in range(1, 5):
#         printNum()

# def needsum(n: int, m: int):
#     """
#     求n和m的和
#     :param n:
#     :param m:
#     :return:
#     """
#     x = 1
#     for i in range(n, m + 1):
#         x += i
#     return x
#
#
# n = int(input("请输入n"))
# m = int(input("请输入m"))
# print(needsum(n, m))

def jiecheng(n: int):
    y = 1
    for i in range(1, n + 1):
        y *= i
    return y


x = int(input("你想求谁的阶乘"))
print(jiecheng(x))


def jiechengSum(m: int):
    z = 0
    for i in range(1, m + 1):
        z += jiecheng(i)
    return z


j = int(input("你想要谁的阶乘和"))
print(jiechengSum(j))
