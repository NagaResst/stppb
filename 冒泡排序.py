numbers = [6, 2, 1, 85, 84, 6, 1, 3, 15, 489, 45, 132, 1, 5, 496]
n = 0
while n < len(numbers) - 1:
    i = 0
    while i < len(numbers) - 1 - n:
        if numbers[i] > numbers[i + 1]:
            numbers[i], numbers[i + 1] = numbers[i + 1], numbers[i]
        i += 1
    n += 1
print(numbers)
# 比较次数优化和完成任务中断
