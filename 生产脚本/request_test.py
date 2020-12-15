import datetime
import os
import time

import requests


class SiteList(object):
    def __init__(self, urls, status_code=0, count=0):
        self.url = urls
        self.code = status_code
        self.count = count

    @staticmethod
    def get_status_code(urls):
        try:
            page = requests.get(urls)
        except:
            return '404'
        return str(page.status_code)

    @staticmethod
    def add_error_count(count):
        count += 1
        return count

    @staticmethod
    def created_ticket(urls, page_code):
        headers = {'content-type': 'application/json', 'TECHNICIAN_KEY': ''}

        post_date = '''{'operation': {'details' : {
                                               'subject' : 'Web Site Service Trouble',
                                               'status' : 'open',
                                               'description' :'Unable to connect to %s ,[%s]',
                                               'requester' : 'Probe_BSU',
                                               'site' : 'SAP-Suning Common Site',
                                               'account' : 'SAP-Suning',
                                               }
                                   }
                      }''' % (urls, page_code)
        msp_api = 'https://hostip/sdpapi/request?format=json&data=' + post_date
        response = requests.post(msp_api, headers, post_date)
        print(response)
        return response


log = "log/" + str(datetime.date.today())


def get_url():
    path = "urls.txt"
    with open(path, 'r') as urls:
        site_url_str = urls.read()
        site_url = site_url_str.split(sep='\n')
        urls.close()
    return site_url


site_list = get_url()
urls_list = []
for urls in site_list:
    url = SiteList(urls)
    urls_list.append(url)

while True:
    # site_list = get_url()
    if os.path.exists(log):
        os.chdir(log)
    else:
        os.makedirs(log)
        os.chdir(log)

    with open('success.log', 'a') as success:
        with open('failed.log', 'a') as failed:
            for url in urls_list:
                # url = SiteList(url)
                code = url.get_status_code(url.url)
                if code == '200':
                    success.write(str(datetime.datetime.now()) + '|success[' + code + ']|' + url.url + '\n')
                    url.count = 0
                # elif code == '300' or code == '301' or code == '302':
                #     pass
                else:
                    failed.write(str(datetime.datetime.now()) + '|failed[' + code + ']|' + url.url + '\n')
                    url.count = url.add_error_count(url.count)
                    print('{}访问失败{}次'.format(url.url, url.count))
                    if url.count == 3:
                        created = url.created_ticket(url.url, code)
            failed.close()
        success.close()
    os.chdir("../..")
    time.sleep(180)
