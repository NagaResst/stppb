#! /bin/python3
# -*- coding:UTF-8 -*-

import requests
import re
import json
import time


class Item(object):
    def __init__(self, name, query_server):
        # 如果玩家输入的指令不是back 就进行对象的初始化
        if self.name != 'back':
            self.name = name
            self.id = None
            self.server = query_server
            # 兼容查询HQ的功能
            self.hq = str(self.name)[-2:]
            if self.hq in ["HQ", "NQ", "hq", "nq"]:
                self.name = str(self.name)[0:-2]
            self.query_item_id()
            self.query_item_price()

    def select_item(self):
        select = input("输入 1 查询售出历史 , 输入 2 查询制作材料 , 输入 3 查询制作成本 \n输入其他道具名继续查询，或输入back返回选择服务器 \n")
        if select == "1":
            self.show_sale_history()
        elif select == "2":
            self.query_item_stuff()
        elif select == "3":
            self.query_item_cost()
        else:
            self.name = select
            self.__init__(self.name, self.server)

    def init_query_result(self, url):
        result = requests.get(url)
        result = result.text.replace('null', '"None"')
        result = json.loads(result)
        lastUploadTime = float(result['lastUploadTime'] / 1000)
        lastUploadTime = self.timestamp_to_time(lastUploadTime)
        return result, lastUploadTime

    @staticmethod
    def timestamp_to_time(timestamp):
        timearray = time.localtime(timestamp)
        res = time.strftime("%Y-%m-%d %H:%M:%S", timearray)
        return res

    @staticmethod
    def hq_or_not(value):
        if value:
            hq = 'HQ'
        else:
            hq = '  '
        return hq

    def query_item_id(self):
        """
        查询官方的物品ID，为后面的查询提供支持
        """
        try:
            query_url = 'https://cafemaker.wakingsands.com/search?indexes=item&string=' + self.name
            result = requests.get(query_url)
            res = re.findall('"ID":([0-9]*)', result.text)
            self.id = res[0]
            print('物品查询中，请稍候...')
        except KeyError:
            print('无法查询到物品ID。')

    def query_item_price(self):
        """
        在线查询物品的售价，因为数据源来源于玩家上报，有一定的迟滞性。
        universalis在进行HQ过滤查询的时候，无法指定查询的数量。
        所以listings和hq两个查询参数不能同时使用，如果同时使用，hq过滤条件就会失效。
        """
        # HQ查询的方法，universalis不支持在过滤HQ查询的时候指定返回的查询数量。
        if self.hq == "HQ" or self.hq == "hq":
            query_url = 'https://universalis.app/api/%s/%s?hq=true' % (self.server, self.id)
        elif self.hq == "NQ" or self.hq == "nq":
            query_url = 'https://universalis.app/api/%s/%s?hq=false' % (self.server, self.id)
        else:
            query_url = 'https://universalis.app/api/%s/%s?listings=30' % (self.server, self.id)
        result, lastUploadTime = self.init_query_result(query_url)
        try:
            print('查询物品 ' + self.name + '\t\t更新时间： ' + lastUploadTime)
            for record in result['listings']:
                hq = self.hq_or_not(record['hq'])
                # uptime = self.timestamp_to_time(record['lastReviewTime'])
                if 'worldName' in record:
                    # print('''单价：%d\t数量：%2d  %s\t总价：%d\t服务器：%-5.4s\t卖家雇员：%s \t\t 上架时间：%s''' % (
                    #     record['pricePerUnit'], record['quantity'], hq, record['total'], record['worldName'],
                    #     record['retainerName'], uptime))
                    print('''单价：%d\t数量：%2d  %s\t总价：%d\t服务器：%-5.4s \t卖家雇员：%s''' % (
                        record['pricePerUnit'], record['quantity'], hq, record['total'], record['worldName'],
                        record['retainerName']))
                else:
                    print('''单价：%d\t数量：%2d  %s\t总价：%d \t卖家雇员：%s''' % (
                        record['pricePerUnit'], record['quantity'], hq, record['total'], record['retainerName']))
            print('\n 以下是最近5次的销售记录')
            for record in result['recentHistory']:
                if record['hq']:
                    hq = 'HQ'
                else:
                    hq = '  '
                buytime = self.timestamp_to_time(record['timestamp'])
                if 'worldName' in record:
                    print('''单价：%d\t数量：%2d  %s\t总价：%d\t服务器：%-5.4s\t买家：%s \t 购买时间：%s''' % (
                        record['pricePerUnit'], record['quantity'], hq, record['total'], record['worldName'],
                        record['buyerName'], buytime))
                else:
                    print('''单价：%d\t数量：%2d  %s\t总价：%d\t\t买家：%s \t 购买时间：%s''' % (
                        record['pricePerUnit'], record['quantity'], hq, record['total'],
                        record['buyerName'], buytime))
            self.select_item()
        finally:
            pass

    def show_sale_history(self):
        """
        在线查询物品的售出历史
        """
        query_url = 'https://universalis.app/api/history/%s/%s?entries=30' % (self.server, self.id)
        result, lastUploadTime = self.init_query_result(query_url)
        print('\n查询物品 ' + self.name + ' 的历史售出记录  \t\t更新时间： ' + lastUploadTime)
        for record in result['entries']:
            hq = self.hq_or_not(record['hq'])
            saletime = self.timestamp_to_time(record['timestamp'])
            if 'worldName' in record:
                print('''单价：%d\t数量：%2d  %s\t总价：%d\t服务器：%-5.4s\t\t 售出时间：%s''' % (
                    record['pricePerUnit'], record['quantity'], hq, (record['pricePerUnit'] * record['quantity']),
                    record['worldName'], saletime))
            else:
                print('''单价：%d\t数量：%2d  %s\t总价：%d\t\t 售出时间：%s''' % (
                    record['pricePerUnit'], record['quantity'], hq, (record['pricePerUnit'] * record['quantity']),
                    saletime))
        self.select_item()

    def query_item_stuff(self):
        """
        查询物品的制作材料
        """
        print('待开发')

    def query_item_cost(self):
        """
        查询物品的制作成本
        """
        print('待开发')


def select_server():
    print('\n请输入要查询的服务器大区,可输入服务器简称，例如“猫、狗、猪、鸟” \n')
    server = input()
    # server = '猫小胖'
    if server == '1' or server == '猫':
        server = '猫小胖'
        print("已经设定服务器为 猫小胖")
    elif server == '鸟':
        server = '陆行鸟'
        print("已经设定服务器为 陆行鸟")
    elif server == '猪':
        server = '莫古力'
        print("已经设定服务器为 莫古力")
    elif server == '狗':
        server = '豆豆柴'
        print("已经设定服务器为 豆豆柴")
    return server


while True:
    selectd_server = select_server
    while True:
        print('请输入要查询的物品全名 , 或输入back返回选择服务器')
        item = input()
        # 查询前使用back，直接返回服务器选择
        if item == 'back':
            break
        item = Item(item, selectd_server)
        # 查询过后使用back，item为实例化之后的对象，item的name属性为back。
        if item.name == 'back':
            break
