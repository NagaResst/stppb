import requests
import time

site_url = ['', '', '', '', '', '']


def get_status_code(url):
    page = requests.get(url)
    return page.status_code


def log(url, status_code, state):
    pass


def created_ticket(url,code):
    header = {}
    post_date = ''
    response = requests.post()
    return response


def test(url):
    code = get_status_code(url)
    if code == 200:
        log(url, code, 'success')
    # elif code == 300 or code == 301 or code == 302:
    #     pass
    else:
        log(url, code, 'failed')
        created_ticket(url, code)


while True:
    for url in site_url:
        test(url)
    time.sleep(180)
