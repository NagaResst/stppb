import requests
import json

url = 'https://5p.nbbjack.com/statics/statics.json'
result = requests.get(url)
result = json.loads(result.content)
print('读取成功')

