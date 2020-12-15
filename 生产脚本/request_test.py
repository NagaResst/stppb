import requests
import datetime
import time
import os

error_count = {}
url_path = "url.txt"
now_date = str(datetime.date.today())
log = "../log/" + now_date
count = 0


def get_url(path):
    with open(path, 'r') as urls:
        site_url_str = urls.read()
        site_url = site_url_str.split(sep='\n')
    urls.close()
    return site_url


def add_error_count(urls):
    global error_count
    global count
    count += 1
    error_count[urls] = count
    return error_count


def get_status_code(urls):
    page = requests.get(urls)
    return page.status_code


def created_ticket(urls, page_code):
    header = {}
    post_date = '' + urls + '' + page_code + ''
    response = requests.post('https://msp.deliverycenter.cn:8088', header, post_date)
    return response


site_list = get_url(url_path)
while True:
    if not os.path.exists(log + '/success.log'):
        os.mknod(log + '/success.log')
        os.mknod(log + '/failed.log')

    with open(log + '/success.log', 'a') as success:
        with open(log + '/failed.log', 'a') as failed:
            for url in site_list:
                code = str(get_status_code(url))
                if code == '200':
                    success.write(str(datetime.datetime.now()) + '|success[' + code + ']|' + url)
                # elif code == '300' or code == '301' or code == '302':
                #     pass
                else:
                    failed.write(str(datetime.datetime.now()) + '|failed[' + code + ']|' + url)
                    add_error_count(url)
                    if error_count[url] > 3:
                        created_ticket(url, code)
        failed.close()
    success.close()
    time.sleep(180)
