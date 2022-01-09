import copy

numbs1 = [100, 200, 300]
numbs2 = numbs1
numbs1[0] = [1]
print(numbs2)
print("%X %X" % (id(numbs2), id(numbs2)))
numbs3 = copy.deepcopy(numbs1)
print("列表的内存地址%X %X %X" % (id(numbs1), id(numbs2), id(numbs3)))
print("列表中第一个元素的内存地址%X %X %X" % (id(numbs1[0]), id(numbs2[0]), id(numbs3[0])))
# 可以使用pythontutor.com在线观看数据的修改流程
