import json

person = {'name': 'jack', 'age': 18, 'gender': 'male'}
m = json.dumps(person)
print(m, ' \n 他的类型是', type(m))
# n = eval(m)
# print(type(n)) #<class 'dict'>
n = json.loads(m)
print(type(n))  # <class 'dict'>

for i, r in enumerate(person):
    print(i, r)
# value 只是用来描述key的属性  想对于字典来说 “key”才是字典真正的“value”
