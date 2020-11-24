x = {"name": 'jacy', "age": '19', "address": 'england'}
y = '大家好，我是{name}，我来自{address}，今年{age}岁了。'
print(y.format(**x))
# 列表和集合可以使用 *x 来遍历每一个变量  或者使用索引
# 字典需要使用 **x
