import pymysql

# 导入数据操作的库
# 连接数据库
db = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='babyplan',
    charset='utf8'
)
# 定义游标
c = db.cursor()
# 执行SQL命令
c.execute("select * from userinfo")
# 获取userinfo表的第一条数据
# record=c.fetchone()
# print(record)
# 获取userinfo表所有数据方法一
'''
record=c.fetchall()
print(record)
'''
# 获取userinfo表所有数据方法二
'''
for i in range(c.rowcount):
  record=c.fetchone()
  print(record)
'''
# 关闭数据库
db.close()
