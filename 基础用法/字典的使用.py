# chars = ['a', 'b', 'a', 's', 'k', 'l', 'd', 'f', 'j', 'a', 'l', 's', 'd', 'j', 'k', 'f', 'l', 'j']
# char_count = {}
# for char in chars:
#     if char not in char_count:
#         char_count[char] = chars.count(char)
# print(char_count)
# x = max(char_count.values())
# print(x)
#
# for k, v in char_count.items():
#     if v == x:
#         print(k)
#
# persons = [
#     {'name': 'zhangsan', 'age': 18},
#     {'name': 'lisi', 'age': 21},
#     {'name': 'wangwu', 'age': 35},
#     {'name': 'zhaoliu', 'age': 31}
# ]
# client_name = input('请输入用户名')
# for person in persons:
#     if person['name'] == client_name:
#         print('您输入的用户名已经存在')
#         break
# else:
#     print('您输入的用户名不存在')
#     y = int(input('请输入您的年龄'))
#     new_persons = {'name': client_name, 'age': y}
#     persons.append(new_persons)
#
#     print(persons)
dict1 = {'a': 100, 'b': 200, 'c': 300}
dict2 = {}
# for k, v in dict1.items():
#     dict2[v] = k
#
# noinspection PyRedeclaration
dict2 = {v: k for k, v in dict1.items()}
print(dict2)
