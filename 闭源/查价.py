# -*- coding:UTF-8 -*-

import requests
import json
import time


class Item(object):
    def __init__(self, name, query_server):
        """
        如果玩家输入的指令不是back 就进行对象的初始化
        """
        self.name = name
        self.id = None
        self.server = query_server
        self.hq = str(self.name)[-2:]
        if self.hq in ["HQ", "NQ", "hq", "nq"]:
            self.name = str(self.name)[0:-2]
        self.start_use()

    def start_use(self):
        if self.name != 'back':
            self.query_item_id()
            self.query_item_price()

    def select_item(self):
        select = input("""
输入 h 查询售出历史 , 输入 m 查询更多记录,  输入 o 显示所有区服的最低价 ,输入 2 查询制作材料 , 输入 3 查询制作成本 
输入其他道具名继续查询，或输入back返回选择服务器 
""")
        if select == "h" or select == "H":
            self.show_sale_history()
        elif select == "m" or select == "M":
            self.show_more_result()
        elif select == "o" or select == "O":
            self.show_every_server()
        elif select == "2":
            self.query_item_stuff()
        elif select == "3":
            self.query_item_cost()
        else:
            self.name = select
            self.__init__(self.name, self.server)

    def select_more_server(self):
        """
        为查询所有区服最低价提供支持
        https://ff.web.sdo.com/web8/index.html#/servers
        """
        server_list = []
        if self.server == '猫小胖':
            server_list = ['紫水栈桥', '延夏', '静语庄园', '摩杜纳', '海猫茶屋', '柔风海湾', '琥珀原']
        elif self.server == '陆行鸟':
            server_list = ['红玉海', '神意之地', '拉诺西亚', '幻影群岛', '萌芽池', '宇宙和音', '沃仙曦染', '晨曦王座']
        elif self.server == '莫古力':
            server_list = ['白银乡', '白金幻象', '神拳痕', '潮风亭', '旅人栈桥', '拂晓之间', '龙巢神殿', '梦羽宝境']
        elif self.server == '豆豆柴':
            server_list = ['水晶塔', '银泪湖', '太阳海岸', '伊修加德', '红茶川']
        return server_list

    def init_query_result(self, url):
        """
        查询结果序列化成字典
        """
        result = requests.get(url)
        # 当属性的值为null的时候，无法转换成字典，将其替换为None
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

    def select_itemid(self, itemlist):
        """
        部分一致关键词搜索支持
        """
        x = 1
        print('编号\t\t\t物品名称')
        for i in itemlist:
            print("%-5.d  \t\t%s " % (x, i['Name']))
            x += 1
        print('请输入要查询的物品编号，输入物品名重新查询')
        select = input()
        if select.isdigit():
            select = (int(select)) - 1
            self.id = itemlist[select]['ID']
            self.name = itemlist[select]['Name']
        else:
            self.__init__(select, self.server)

    def query_item_id(self):
        """
        查询官方的物品ID，为后面的查询提供支持
        后续可能使用 garlandtools 替换现在的查询接口
        https://garlandtools.cn/api/search.php?text=%E6%B0%B4%E4%B9%8B%E6%99%B6%E7%B0%87&lang=chs&ilvlMin=1&ilvlMax=999
        """
        try:
            query_url = 'https://cafemaker.wakingsands.com/search?indexes=item&string=' + self.name
            print('物品查询中，请稍候...')
            result = requests.get(query_url)
            itemstr = result.text.replace('null', '"None"')
            itemde = (json.loads(itemstr))["Results"]
            if len(itemde) == 1:
                self.id = itemde[0]['ID']
                self.name = itemde[0]['Name']
            elif len(itemde) > 1:
                self.select_itemid(itemde)
        except KeyError:
            print('无法查询到物品ID。')

    def show_result(self, result, server=None):
        """
        显示查询结果
        """
        for record in result['listings']:
            hq = self.hq_or_not(record['hq'])
            # uptime = self.timestamp_to_time(record['lastReviewTime'])
            if 'worldName' in record:
                print('''单价：%d\t数量：%2d  %s\t总价：%-8d\t服务器：%-5.4s \t卖家雇员：%s''' % (
                    record['pricePerUnit'], record['quantity'], hq, record['total'], record['worldName'],
                    record['retainerName']))
            elif server is not None:
                print('''单价：%d\t数量：%2d  %s\t总价：%-8d\t服务器：%-5.4s \t卖家雇员：%s''' % (
                    record['pricePerUnit'], record['quantity'], hq, record['total'], server, record['retainerName']))
            else:
                print('''单价：%d\t数量：%2d  %s\t总价：%-8d \t卖家雇员：%s''' % (
                    record['pricePerUnit'], record['quantity'], hq, record['total'], record['retainerName']))
        return result

    def query_item_price(self):
        """
        在线查询物品的售价，因为数据源来源于玩家上报，有一定的迟滞性。
        universalis在进行HQ过滤查询的时候，无法指定查询的数量。
        所以listings和hq两个查询参数不能同时使用，如果同时使用，hq过滤条件就会失效。
        """
        if self.hq == "HQ" or self.hq == "hq":
            query_url = 'https://universalis.app/api/%s/%s?hq=true' % (self.server, self.id)
        elif self.hq == "NQ" or self.hq == "nq":
            query_url = 'https://universalis.app/api/%s/%s?hq=false' % (self.server, self.id)
        else:
            query_url = 'https://universalis.app/api/%s/%s?listings=15' % (self.server, self.id)
        try:
            result, lastUploadTime = self.init_query_result(query_url)
            print('查询物品 ' + self.name + '\t\t更新时间： ' + lastUploadTime)
            self.show_result(result)
            print('\n 以下是最近5次的销售记录')
            for record in result['recentHistory']:
                hq = self.hq_or_not(record['hq'])
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
        except KeyError:
            print('查询不到物品数据')

    def show_every_server(self):
        """
        查询当前大区每个服务器的最低价
        """
        servers_list = self.select_more_server()
        for server in servers_list:
            query_url = 'https://universalis.app/api/%s/%s?listings=1' % (server, self.id)
            result, lastUploadTime = self.init_query_result(query_url)
            self.show_result(result, server)
        self.select_item()

    def show_more_result(self):
        """
        显示更多在板子上售卖的商品
        """
        query_url = 'https://universalis.app/api/%s/%s?listings=50' % (self.server, self.id)
        result, lastUploadTime = self.init_query_result(query_url)
        print('查询物品 ' + self.name + '\t\t更新时间： ' + lastUploadTime)
        self.show_result(result)
        self.select_item()

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

    @staticmethod
    def query_item_detial(itemid):
        query_url = 'https://garlandtools.cn/api/get.php?type=item&lang=chs&version=3&id=' + str(itemid)
        result = requests.get(query_url)
        result = (json.loads(result.text))['item']
        return result

    def query_item_stuff(self):
        """
        查询物品的制作材料
        """
        print('正在查询制作需要的素材')
        result = self.query_item_detial(self.id)
        result = result['craft'][0]['ingredients']
        for stuff in result:
            item_info = self.query_item_detial(stuff['id'])
            print('%s  %-2d' % (item_info['name'], stuff['amount']))
            try:
                c_s_result = self.query_item_detial(stuff['id'])
                c_s_result = c_s_result['craft'][0]['ingredients']
                for l2_stuff in c_s_result:
                    c_item_info = self.query_item_detial(l2_stuff['id'])
                    print('\t%s  %-2d' % (c_item_info['name'], l2_stuff['amount']))
                    try:
                        cc_s_result = self.query_item_detial(l2_stuff['id'])
                        cc_s_result = cc_s_result['craft'][0]['ingredients']
                        for l3_stuff in cc_s_result:
                            cc_item_info = self.query_item_detial(l3_stuff['id'])
                            print('\t\t%s  %-2d' % (cc_item_info['name'], l3_stuff['amount']))
                    except KeyError:
                        pass
            except KeyError:
                pass

    def query_item_cost(self):
        """
        查询物品的制作成本
        """
        print('待开发')


def select_server():
    server = input('\n请输入要查询的服务器大区,可输入服务器简称，例如“猫、狗、猪、鸟” \n')
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
    selectd_server = select_server()
    # selectd_server = '猫小胖'
    while True:
        print('请输入要查询的物品全名 , 或输入back返回选择服务器')
        item = input()
        # item = '夹层'
        # 查询前使用back，直接返回服务器选择
        if item == 'back':
            break
        item = Item(item, selectd_server)
        # 查询过后使用back，item为实例化之后的对象，item的name属性为back。
        if item.name == 'back':
            break
