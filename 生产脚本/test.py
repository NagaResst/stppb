import datetime
import os
from time import sleep
import requests


class SiteList(object):
    def __init__(self, urls, status_code='0', count=0):
        self.url = urls
        self.code = status_code
        self.count = count

    def get_status_code(self):
        try:
            page = requests.get(self.url)
            self.code = str(page.status_code)
        except:
            self.code = 'time out'

    def add_error_count(self):
        self.count += 1

    @staticmethod
    def created_ticket(urls, page_code):
        headers = {'content-type': 'application/json', 'TECHNICIAN_KEY': ''}
        now = str(datetime.datetime.now())
        post_date = '''{'operation': {'details' : {
                                               'subject' : 'Web Site Service Trouble',
                                               'status' : 'open',
                                               'description' :'Unable to connect to %s ,[%s] at %s',
                                               'requester' : 'Probe_BSU',
                                               'site' : 'SAP-Suning Common Site',
                                               'account' : 'SAP-Suning',
                                               }
                                   }
                      }''' % (urls, page_code, now)
        msp_api = 'https://hostip/sdpapi/request?format=json&data=' + post_date
        response = requests.post(msp_api, headers, post_date)
        print(response)
        return response

    def test_url(self, success, failed):
        self.get_status_code()
        if self.code == '200':
            success.write(str(datetime.datetime.now()) + '|success[' + self.code + ']|' + url.url + '\n')
            success.flush()
            # 如果以前不可以访问，现在可以访问就初始化失败次数
            self.count = 0
        else:
            failed.write(str(datetime.datetime.now()) + '|failed[' + self.code + ']|' + url.url + '\n')
            failed.flush()
            self.add_error_count()
            print('{}访问失败{}次'.format(self.url, self.count) + '\n')
            # 访问失败3次就到MSP创建工单
            if self.count == 3:
                self.created_ticket(self.url, self.code)


def get_url():
    path = "urls.txt"
    with open(path, 'r') as urls:
        site_url_str = urls.read()
        site_url = site_url_str.split(sep='\n')
        site_list = [i for i in site_url if i != '']
        urls.close()
    return site_list


def init_object():
    site_list = get_url()
    urls_list = []
    for urls in site_list:
        url = SiteList(urls)
        urls_list.append(url)
    return urls_list, site_list


urls_list, site_list = init_object()
while True:
    with open('run.log', 'a') as runlog:
        log = "log/" + str(datetime.date.today())
        # 重载列表 如果发生变化就重新初始化实例
        site_list_new = get_url()
        if site_list != site_list_new:
            urls_list, site_list = init_object()
        # 判断日志文件夹是否存在，如果不存在就创建
        # 只判断了文件夹，没有判断日志文件，如果存在文件夹不存在日志，在linux上的兼容性没有测试，不排除会出问题
        runlog.write('reload list | {}'.format(datetime.datetime.now()) + '\n')
        if os.path.exists(log):
            os.chdir(log)
        else:
            os.makedirs(log)
            os.chdir(log)
        runlog.write('ready for open file | {}'.format(datetime.datetime.now()) + '\n')
        runlog.flush()
        with open('success.log', 'a') as success:
            with open('failed.log', 'a') as failed:
                for url in urls_list:
                    url.test_url(success, failed)
            failed.close()
        success.close()
        runlog.write('close file | {}'.format(datetime.datetime.now()) + '\n')
        os.chdir("../..")
        runlog.write('work done | {}'.format(datetime.datetime.now()) + '\n')
    runlog.close()
    sleep(180)
