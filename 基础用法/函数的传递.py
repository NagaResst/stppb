students = [
    {'name': '张三', 'age': '18', 'score': '99', },
    {'name': '李四', 'age': '18', 'score': '96', },
    {'name': '王五', 'age': '18', 'score': '95', },
    {'name': '赵六', 'age': '18', 'score': '93', },
    {'name': 'Code', 'age': '18', 'score': '95', },
    {'name': 'Martin', 'age': '18', 'score': '97', },
    {'name': 'Alex', 'age': '18', 'score': '98', }
]


# # foo()函数返回了字典中的score元素的属性
# def foo(ele):
#     return ele['score']
#
#
# # 当使用sort排序的时候key=foo方法返回的属性是个字符串，可以使用"<"进行排序
# students.sort(reverse=True, key=foo)

# 如果使用lambda表达式那么写法如下：
students.sort(reverse=True, key=lambda x: x['score'])
print(students)

