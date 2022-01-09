#!/usr/bin/python
x = int(input('请输入第一个数字'))
y = int(input('请输入第二个数字'))
z = x - y
if z % 2 != 0:
    print(z)
else:
    print('结果不是奇数')
j = 0
while j <= 100:
    if j % 2 == 0:
        print(j)
    j += 1
k = 0
for i in range(1, 101):
    if i % 10 == 2 and i % 3 == 0:
        k += 1
print('个数为', k)
for i in range(101, 201):
    for j in range(2, i):
        if i % j == 0:
            break
    else:
        print(i)
for x in range(0, 100 // 3 + 1):
    for y in range(0, 100 // 2 + 1):
        if x * 3 + y * 2 + (100 - x - y) / 2 == 100:
            print(x, y, (100 - x - y))

count = 0
while 2 ** count * 0.08 <= 8848130:
    count += 1
print(count)
