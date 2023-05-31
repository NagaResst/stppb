import requests
import json
import datetime

# 获取 token
path = 'https://url/api.php/v1'
body = {"account": "", "password": ""}
url = path + "/tokens"
token = json.loads(requests.post(url=url, json=body).text)['token']
header = {"Token": token}
# print(token)

# 添加用户
url = path + "/users"
date_today = datetime.datetime.now().strftime("%Y-%m-%d")
user_list = [
    {"account": "username", "password": "password", "realname": "",
     "dept": 1, "role": "dev", "gender": "m", "join": date_today}
]

for i in user_list:
    result = requests.post(url=url, headers=header, json=i)
    print(result.text)

# 脚本用完了需要进系统给用户添加权限
