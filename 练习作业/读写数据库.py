import pymysql

# 导入数据操作的库
# 连接数据库
db = pymysql.connect(
    host='192.168.10.100',
    port=4000,
    user='uupa',
    password='lingchuan',
    database='uupa',
    charset='utf8'
)
# 定义游标
c = db.cursor()
# 执行SQL命令
c.execute("select user_id from mid")
# 获取userinfo表的第一条数据
# record=c.fetchone()
# print(record)
# 获取userinfo表所有数据方法一
record = c.fetchall()
print(record)
re_list = []
# for i in record:
#     re_list.append(i[0])
for i in record:
    re_list.append(list(i))
# re_list = list(record)
for i in re_list:
    if '802a3ee47f25784888d189d13853a90c97318bc00d4ffa76e161ed157b09f170' in i:
        print('yes , it in ')
# 获取userinfo表所有数据方法二
'''
for i in range(c.rowcount):
  record=c.fetchone()
  print(record)
'''
# 关闭数据库
db.close()
