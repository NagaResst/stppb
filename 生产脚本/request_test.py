import requests


def get_status_code(url):
    page = requests.get(url)
    return page.status_code


url = 'https://s1.bsu.edu.cn'
print(get_status_code(url))