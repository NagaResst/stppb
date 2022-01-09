x = {"name": 'jacy', "age": '19', "address": 'england'}
y = '大家好，我是{name}，我来自{address}，今年{age}岁了。'
print(y.format(**x))
# 列表和集合可以使用 *x 来遍历每一个变量  或者使用索引
# 字典需要使用 **x

word = """hello
world ,
engineer"""
word = word.replace('world ,\n', '')
print(word)

# x = "asdf,asdfasd,fasdf. asdf,sddafas,dgasd,fasdf"
# y = x.split(',')
# print(y)
# y.remove('fasdf')
# print(y)
# print(x[1:2])
# print(x.capitalize())
# word = "test"
# print(word.ljust(len(word) + 1, '+').rjust(len(word) + 2, 'k'))
# print(word.center(len(word) + 2, '@'))
names = 'zhangsan,lisi,wangwu,jack,tony,lily'
names = names.split(',')
print(names, 'over')
# for names in names:
#     print(names)
print(names, type(names))
names = ' & '.join(names)
print(names)
type(names)
