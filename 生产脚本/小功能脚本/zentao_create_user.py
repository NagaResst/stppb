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
user_list = [
    {"account": "username", "password": "passwd", "realname": "","dept": 10, "role": "dev","gender":"m", "join": date_today},
    {"account": "username", "password": "passwd", "realname": "","dept": 10, "role": "dev","gender":"m", "join": date_today},
    {"account": "username", "password": "passwd", "realname": "","dept": 10, "role": "dev","gender":"m", "join": date_today},
    {"account": "username", "password": "passwd", "realname": "","dept": 10, "role": "dev","gender":"m", "join": date_today},
    {"account": "username", "password": "passwd", "realname": "","dept": 10, "role": "dev","gender":"m", "join": date_today}
]

for i in user_list:
    result = requests.post(url=url, headers=header, json=i)
    print(result.text)
