import requests
import json
import datetime

# 获取 token
path = 'https://server_name/www/api.php/v1'
body = {"account": "", "password": ""}
url = path + "/tokens"
token = json.loads(requests.post(url=url, json=body).text)['token']
header = { "Token": token}
# print(token)

# 添加用户
url = path + "/users"
date_today = datetime.datetime.now().strftime("%Y-%m-%d")
data = {"account": "username", "password": "passwd", "realname": "",
"dept": 10, "role": "dev","gender":"m", "join": date_today}
result = requests.post(url=url, headers=header, json=data)
print(result.text)


# 脚本用完了需要进系统给用户添加权限


#  部门编号
# 1	咨询事业部
# 2	项目事业部
# 3	研发部
# 4	智慧物资部
# 5	大数据部
# 6	孵化部
# 7	业务一部
# 8	业务二部
# 9	业务三部
# 10	外聘研发
# 11	离职员工
# 12	共享服务
# 13	综合部
# 14	客户
# 15	共享公司

