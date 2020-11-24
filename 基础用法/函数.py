def printNum():
    print('1')
    print('2')
    print('3')
    print('4')
    print('5')


num = int(input('请输入数字'))
if 0 <= num <= 10:
    printNum()
elif 10 < num <= 20:
    printNum()
    printNum()
else:
    for i in range(1, 5):
        printNum()
