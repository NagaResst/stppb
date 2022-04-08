#! /bin/python3
import datetime
import os
from time import sleep
import requests


# 定义站点列表这个类 需要的内容包括http状态码和访问次数，以及对应的方法
class SiteList(object):
    def __init__(self, urls, status_code='0', count=0):
        self.url = urls
        self.code = status_code
        self.count = count

    # 获取当前站点的http状态码
    def get_status_code(self):
        try:
            page = requests.get(self.url)
            self.code = str(page.status_code)
        except Exception:
            self.code = 'time out'

    # 如果站点无法访问那么在访问次数上+1
    def add_error_count(self):
        self.count += 1

    @staticmethod
    def created_ticket(urls, page_code):
        # 当网站不可访问时用来创建工单的函数 需要使用MSP的技术员密钥
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
            # 访问结果直接写日志
            success.write(str(datetime.datetime.now()) + '|success[' + self.code + ']|' + self.url + '\n')
            # 日志内容直接持久化到磁盘
            success.flush()
            # 如果以前不可以访问，现在可以访问就初始化失败次数
            self.count = 0
        else:
            failed.write(str(datetime.datetime.now()) + '|failed[' + self.code + ']|' + self.url + '\n')
            failed.flush()
            self.add_error_count()
            print('{}访问失败{}次'.format(self.url, self.count) + '\n')
            # 访问失败3次就到MSP创建工单
            if self.count == 3:
                self.created_ticket(self.url, self.code)


def get_url():
    path = "urls.txt"
    # 从文件直接读取站点列表，按照行将字符串切割成列表的元素
    with open(path, 'r') as urls:
        site_url_str = urls.read()
        site_url = site_url_str.split(sep='\n')
        # 将所有切割完的元素加入列表
        site_list = [i for i in site_url if i != '']
        urls.close()
    return site_list


def init_object(site_list_old=None):
    # 首次启动的时候会初始化所有监控网站的对象，并将所有对象加入一个列表
    # 如果监控的网站的列表改变了，就重新执行一次初始化操作
    site_list = get_url()
    urls_list = []
    # if site_list != site_list_old:
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
            urls_list, site_list = init_object(site_list)
        # 判断日志文件夹是否存在，如果不存在就创建
        # 只判断了文件夹，没有判断日志文件，如果存在文件夹不存在日志，在linux上的兼容性没有测试，不排除会出问题
        runlog.write('load list | {}'.format(datetime.datetime.now()) + '\n')
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
