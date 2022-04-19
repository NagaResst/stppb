# -*- coding:UTF-8 -*-

from requests import get
from json import loads
from time import localtime, strftime


# from math import ceil


class ItemQuerier(object):
    def __init__(self, name, query_server):
        """
        对象初始化
        """
        self.name = name
        self.id = None
        self.stuff = {}
        self.d_cost = 0
        self.o_cost = 0
        self.server = query_server
        self.hq = str(self.name)[-2:]
        if self.hq in ["HQ", "NQ", "hq", "nq"]:
            self.name = str(self.name)[0:-2]

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

    @staticmethod
    def init_query_result(url):
        """
        查询结果序列化成字典
        """
        result = get(url)
        # 当属性的值为null的时候，无法转换成字典，将其替换为None
        result = result.text.replace('null', '"None"')
        result = loads(result)
        return result

    @staticmethod
    def timestamp_to_time(timestamp):
        """
        时间戳转换工具
        """
        if timestamp > 9999999999:
            timestamp = float(timestamp / 1000)
        timearray = localtime(timestamp)
        res = strftime("%Y-%m-%d %H:%M:%S", timearray)
        return res

    @staticmethod
    def hq_or_not(value):
        """
        HQ占位符
        """
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
        user_select = input()
        if user_select.isdigit():
            user_select = (int(user_select)) - 1
            self.id = itemlist[user_select]['ID']
            self.name = itemlist[user_select]['Name']
        else:
            self.__init__(user_select, self.server)

    def query_item_id(self):
        """
        查询官方的物品ID，为后面的查询提供支持
        后续可能使用 garlandtools 替换现在的查询接口
        https://garlandtools.cn/api/search.php?text=%E6%B0%B4%E4%B9%8B%E6%99%B6%E7%B0%87&lang=chs&ilvlMin=1&ilvlMax=999
        """
        try:
            query_url = 'https://cafemaker.wakingsands.com/search?indexes=item&string=' + self.name
            print('\n猴面雀正在为您查找需要的数据，请稍候... ')
            result = get(query_url)
            itemstr = result.text.replace('null', '"None"')
            itemde = (loads(itemstr))["Results"]
            if len(itemde) == 1:
                self.id = itemde[0]['ID']
                self.name = itemde[0]['Name']
            elif len(itemde) > 1:
                self.select_itemid(itemde)
            else:
                print('\n猴面雀没有找到到您要查找的物品。')
            print('猴面雀已经为您查找到物品 %s ID：%d' % (self.name, self.id))
        except ConnectionError:
            print('\n猴面雀发现网络有点问题，找不到想要的资料了')

    def show_result(self, result, server=None):
        """
        显示查询结果
        """
        for record in result['listings']:
            hq = self.hq_or_not(record['hq'])
            # uptime = self.timestamp_to_time(record['lastReviewTime'])
            if 'worldName' in record:
                print('''单价：%-6d\t数量：%2d  %s\t总价：%-8d\t服务器：%-5.4s \t卖家雇员：%s''' % (
                    record['pricePerUnit'], record['quantity'], hq, record['total'], record['worldName'],
                    record['retainerName']))
            elif server is not None:
                print('''单价：%-6d\t数量：%2d  %s\t总价：%-8d\t服务器：%-5.4s \t卖家雇员：%s''' % (
                    record['pricePerUnit'], record['quantity'], hq, record['total'], server, record['retainerName']))
            else:
                print('''单价：%-6d\t数量：%2d  %s\t总价：%-8d \t卖家雇员：%s''' % (
                    record['pricePerUnit'], record['quantity'], hq, record['total'], record['retainerName']))
        return result

    def query_item_price(self):
        """
        在线查询物品的售价，因为数据源来源于玩家上报，有一定的迟滞性。
        universalis在进行HQ过滤查询的时候，无法指定查询的数量。
        所以listings和hq两个查询参数不能同时使用，如果同时使用，hq过滤条件就会失效。
        """
        self.query_item_id()
        if self.id is None:
            pass
        else:
            if self.hq == "HQ" or self.hq == "hq":
                query_url = 'https://universalis.app/api/v2/%s/%s?listings=15&hq=true' % (self.server, self.id)
            elif self.hq == "NQ" or self.hq == "nq":
                query_url = 'https://universalis.app/api/v2/%s/%s?listings=15&hq=false' % (self.server, self.id)
            else:
                query_url = 'https://universalis.app/api/%s/%s?listings=15' % (self.server, self.id)
            try:
                result = self.init_query_result(query_url)
                lastUploadTime = self.timestamp_to_time(result['lastUploadTime'])
                print('\n猴面雀为您查找到 ' + self.name + ' 的最新在售信息。\t\t更新时间： ' + lastUploadTime)
                self.show_result(result)
                print('\n 以下是最近5次的售出记录')
                for record in result['recentHistory']:
                    hq = self.hq_or_not(record['hq'])
                    buytime = self.timestamp_to_time(record['timestamp'])
                    if 'worldName' in record:
                        print('''单价：%-6d\t数量：%2d  %s\t总价：%-8d\t服务器：%-5.4s\t买家：%-6s \t 购买时间：%s''' % (
                            record['pricePerUnit'], record['quantity'], hq, record['total'], record['worldName'],
                            record['buyerName'], buytime))
                    else:
                        print('''单价：%-6d\t数量：%2d  %s\t总价：%-8d\t\t买家：%-6s \t\t 购买时间：%s''' % (
                            record['pricePerUnit'], record['quantity'], hq, record['total'],
                            record['buyerName'], buytime))
            except ConnectionError:
                print('\n猴面雀发现网络有点问题，找不到想要的资料了')

    def show_every_server(self):
        """
        查询当前大区每个服务器的最低价
        """
        servers_list = self.select_more_server()
        for server in servers_list:
            result = self.query_item_cost_min(server, self.id, count=1)
            self.show_result(result, server)

    def show_more_result(self):
        """
        显示更多在板子上售卖的商品
        """
        result = self.query_item_cost_min(self.server, self.id, count=50)
        lastUploadTime = self.timestamp_to_time(result['lastUploadTime'])
        print('\n猴面雀为您查找到 ' + self.name + ' 的50条在售信息。 \t更新时间： ' + lastUploadTime)
        self.show_result(result)

    def show_sale_history(self):
        """
        在线查询物品的售出历史
        """
        query_url = 'https://universalis.app/api/history/%s/%s?entries=30' % (self.server, self.id)
        result = self.init_query_result(query_url)
        # lastUploadTime = float(result['lastUploadTime'] / 1000)
        lastUploadTime = self.timestamp_to_time(result['lastUploadTime'])
        print('\n猴面雀为您查找到 ' + self.name + ' 的30条售出历史。 \t更新时间： ' + lastUploadTime)
        for record in result['entries']:
            hq = self.hq_or_not(record['hq'])
            saletime = self.timestamp_to_time(record['timestamp'])
            if 'worldName' in record:
                print('''单价：%-6d\t数量：%2d  %s\t总价：%-8d\t服务器：%-5.4s\t\t 售出时间：%s''' % (
                    record['pricePerUnit'], record['quantity'], hq, (record['pricePerUnit'] * record['quantity']),
                    record['worldName'], saletime))
            else:
                print('''单价：%-6d\t数量：%2d  %s\t总价：%-8d\t\t 售出时间：%s''' % (
                    record['pricePerUnit'], record['quantity'], hq, (record['pricePerUnit'] * record['quantity']),
                    saletime))

    @staticmethod
    def query_item_detial(itemid):
        """
        查询物品的详细信息，查询制作配方和统计成本的前置方法
        """
        try:
            query_url = 'https://garlandtools.cn/api/get.php?type=item&lang=chs&version=3&id=' + str(itemid)
            result = get(query_url)
            result = loads(result.text)
            return result['item']
        except ConnectionError:
            print("\n猴面雀发现网络有点问题，找不到想要的资料了")

    def show_item_craft(self, stuff_list, tab=''):
        """
        展示物品的制作配方
        """
        if self.stuff is not None:
            for stuff in stuff_list:
                if 'priceFromNpc' in stuff:
                    print('%s%-8s\t数量：%d\t价格：%-6d\t%d(npc)' % (
                        tab, stuff['name'], stuff['amount'], stuff['pricePerUnit'], stuff['priceFromNpc']))
                else:
                    print('%s%-8s\t数量：%d\t价格：%-6d' % (tab, stuff['name'], stuff['amount'], stuff['pricePerUnit']))
                if 'craft' in stuff:
                    self.show_item_craft(stuff['craft'], tab=tab + '\t')
        else:
            print('猴面雀发现你要查询的物品不是制作出来的。')

    def query_item_cost_min(self, server, itemid, count):
        """
        查询单项物品的板子价格
        """
        try:
            query_url = 'https://universalis.app/api/%s/%s?listings=%d' % (server, itemid, count)
            result = self.init_query_result(query_url)
            return result
        except ConnectionError:
            print("\n猴面雀发现网络有点问题，找不到想要的资料了")

    def make_item_craft(self, stuff_list):
        """
        统计物品的制作材料
        """
        i = 0
        for unit in stuff_list:
            print('.', end='')
            result = self.query_item_detial(unit['id'])
            stuff_list[i]['name'] = result['name']
            stuff_list[i]['pricePerUnit'] = self.query_item_cost_min(self.server, unit['id'], count=1)['listings'][0][
                'pricePerUnit']
            if 'vendors' in result:
                stuff_list[i]['priceFromNpc'] = result['price']
            if 'craft' in result:
                stuff_list[i]['craft'] = result['craft'][0]['ingredients']
                if 'yield' in result['craft'][0]:
                    stuff_list[i]['yield'] = result['craft'][0]['yield']
                self.make_item_craft(stuff_list[i]['craft'])
            i += 1

    def query_item_craft(self):
        """
        查询物品的制作材料
        """
        if self.stuff is not None:
            if len(self.stuff) == 0:
                print('\n猴面雀正在为您查找制作需要的素材，配方越复杂，猴面雀就需要翻阅越多的资料！')
                self.stuff = self.query_item_detial(self.id)
                if 'craft' in self.stuff:
                    self.stuff = self.stuff['craft'][0]['ingredients']
                    self.make_item_craft(self.stuff)
                    print("\n 猴面雀已经为您查找到 %s 的制作配方" % self.name)
                else:
                    self.stuff = None

    # def query_item_cost(self, stuff_list, count=1, tab=''):
    #     """
    #     查询物品的制作成本的计算器
    #     """
    #     d_cost = 0
    #     self.query_item_craft()
    #     for stuff in stuff_list:
    #         n_count = (stuff['amount'] * count)
    #         if 'priceFromNpc' in stuff:
    #             price = min(stuff['priceFromNpc'], stuff['pricePerUnit']) * n_count
    #         else:
    #             price = stuff['pricePerUnit'] * n_count
    #         print('%s%-8s\t数量%2d\t价格：%-6d' % (tab, stuff['name'], n_count, price))
    #         d_cost = d_cost + price
    #         if 'yield' in stuff and 'craft' in stuff:
    #             c_count = 0
    #             if n_count > stuff['yield']:
    #                 c_count = ceil(n_count / stuff['yield'])
    #             elif n_count <= stuff['yield']:
    #                 c_count = 1
    #             self.o_cost = self.o_cost + self.query_item_cost(stuff['craft'], c_count, tab=tab + '\t')
    #         elif 'craft' in stuff and 'yield' not in stuff:
    #             self.o_cost = self.o_cost + self.query_item_cost(stuff['craft'], n_count, tab=tab + '\t')
    #         else:
    #             self.o_cost = self.o_cost + price
    #     return d_cost

    # def show_item_cost(self):
    #     """
    #     显示物品的制作成本的外壳
    #     """
    #     if self.stuff is not None:
    #         self.d_cost = 0
    #         self.o_cost = 0
    #         print('\n开始统计 %s 制作成本' % self.name)
    #         self.d_cost = self.query_item_cost(self.stuff)
    #         if self.d_cost == self.o_cost:
    #             print('\n材料总价合计 %d' % self.d_cost)
    #         else:
    #             print('\n直接材料总价合计 %d, \t 原始材料价格总价合计 %d' % (self.d_cost, self.o_cost))
    #     else:
    #         print('\n猴面雀发现你要查询的物品不能制作！')


def select_server():
    """
    服务器选择
    """
    server = input('请输入要查询的大区服务器,可输入大区简称，例如“ 1 猫、2 鸟、3 猪、4 狗 ” \n')
    if server == '1' or server == '猫':
        server = '猫小胖'
        print("猴面雀将为您查询 猫小胖 的市场数据")
    elif server == '2' or server == '鸟':
        server = '陆行鸟'
        print("猴面雀将为您查询 陆行鸟 的市场数据")
    elif server == '3' or server == '猪':
        server = '莫古力'
        print("猴面雀将为您查询 莫古力 的市场数据")
    elif server == '4' or server == '狗':
        server = '豆豆柴'
        print("猴面雀将为您查询 豆豆柴 的市场数据")
    else:
        print('猴面雀将为您查询 %s 的市场数据' % server)
    return server


def load_location_list():
    try:
        print("猴面雀正在查找你的本地清单")
        with open(r'FF14价格查询清单.txt', 'r') as list_file:
            list_text = list_file.read()
            item_list = list_text.split('\n')
        return item_list
    except IOError:
        with open(r'FF14价格查询清单.txt', 'w') as list_file:
            list_file.write('')
        print('同目录下没有找到“FF14价格查询清单.txt” ，已为您生成空文件，一行写入一个物品')


def select_locaiton_item(item_list):
    if item_list is None:
        print("本地清单中没有内容呢")
        return None
    else:
        i = 1
        print("请选择需要查询的物品")
        for this_item in item_list:
            print("%-4d\t%s" % (i, this_item))
            i += 1
        selectd_item = int(input())
        print("已选择 %s" % item_list[selectd_item - 1])
        return item_list[selectd_item - 1]


def logo():
    print("""
.........................................................................
................................@@@@\`..]/@@@@@^..]]]]...................
................................=@@@@@@@@@@@@@@@@@@@@@@@.................
.................................@@@@@@@@@@@@@@@@@@@@@@..................
................................/@@@@@@@@@@@@@@@@@@@@@^..................
.............................,/@@@@@@@@@@@@@@@@@@@@@@@@@]................
..........................]@@@@O@O@@@@@@@@@@@@@@@@@@@OO@@@\..............
.......................]@@@@OOOOOOOO@@@@@@@OOOOOOOOOOOOOO@@@\`...........
....................,/@@OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO@@\..........
..................]@@@OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO@@@\........
................/@@@@@O@@@@@@OOOOOOOOOOOOOOOO@@@@@@@@@@OOOOOOOO@@@`......
.............,@@@`...........,\@@OOOOOOO@@@[`..........[@@@OOOOOO@@\.....
............/@`...]/@@@@]`......\@@OO@@O.......]]]]]`.....,@@OOOOO@@@`...
..........,@/..]@@/`.....@@^......@@@/....../@@/[[`.[@@@\`..,@@OOOO@@@`..
.........@@`.=@/.,/@@@@\..=@`.....=@`.....,@/.,@@@@@@@`.,@\...\@OOOOO@@`.
.......,@@../@.,@@@@@@@@^..@^.............@@.*@@@@@@@@@O..@O...,@@OOOO@@`
......=@O..=@..@@@@@@@@@`.,@^.............=\.,@@@@@@@@@@^.=@....,@@OOOO@@
.....=@/...=O..@@@@@@@@...O@..............=@`.\@@@@@@@@@^.=@^....,@OOOO@@
....=@^....,@`.,@@@@[..../@`...............,@^..O@@@@@@[../@......\@OOOO@
....@^......,@\`......]O@/.../^......./`.....\@]........./@`......=@@OOOO
.../@^.........\@@@@@@[.....=@.../@\..=@.......[\@@@@@@@@`........=@@OOOO
..=@@^......................,O@@@`,\@@@/..........................=@@OOOO
.,@@@^................................ ...........................=@OOOOO
./@O@O............................................................O@OOOOO
.@@@@@`..........................................................=@@OOOOO
=@@@O@\........................................ .................O@OOOOOO
=@@@@O@^......*...,]`.................................. ........O@OOOOOOO
/@@@@@@@^....O@@@@@@@O.......]`...]]........=@\..,/@\..........@@OOOOOOOO
@@@@@@@@@O...=@@@@@@O.......=@@@O@@@`.......=@@@/@@@`........=@@OOOOOOOOO
@@@@@@@@@@....,O@@O`.........\@@@@@/.........\@@@@O`......../@OOOOOOOOOOO
@@@@@@@@@^.....................[O@/............[/`..........=@@OOOOOOOOO@
=@@@@@@@@....................................................=@@@O@@@O@O@
========   欢迎使用猴面雀价格查询小工具    夕山菀@紫水栈桥   ============
""")


# ========     老婆！ 是老婆啊！！    琉森@紫水栈桥 专用版     ============


while True:
    logo()
    selectd_server = select_server()
    # if selectd_server is None:
    #     selectd_server = select_server()
    while True:
        print('请输入要查询的物品全名 , 或输入back返回选择服务器 \n')
        item = input()
        # 查询前使用back，直接返回服务器选择
        if item == 'back':
            # selectd_server = None
            break
        # elif item == 'l' or item == 'L':
        #     items = load_location_list()
        #     item = select_locaiton_item(items)
        else:
            if item is None or item == b'\n' or item == '':
                pass
            else:
                item = ItemQuerier(item, selectd_server)
                item.query_item_price()
                while True:
                    if item.id is None:
                        break
                    select = input("""
输入 h 查询售出历史 , 输入 m 查询更多出售信息,  输入 o 显示所有区服的最低价 , 输入 2 查询制作材料 
输入其他道具名继续查询，或输入back返回选择服务器 \n
""")
                    # 输入 2 查询制作材料 , 输入 3 查询制作成本 , 输入 l 查询本地清单
                    if select == 'back':
                        break
                    elif select == "h" or select == "H":
                        item.show_sale_history()
                    elif select == "m" or select == "M":
                        item.show_more_result()
                    elif select == "o" or select == "O":
                        item.show_every_server()
                    elif select == "2":
                        item.query_item_craft()
                        item.show_item_craft(item.stuff)
                    elif select == b'\n' or select == '':
                        pass
                    # elif select == "3":
                    #     item.query_item_craft()
                    #     item.show_item_cost()
                    # elif select == 'l' or item == 'L':
                    #     items = load_location_list()
                    #     item = select_locaiton_item(items)
                    #     item = ItemQuerier(item, selectd_server)
                    #     item.query_item_price()
                    else:
                        item = select
                        item = ItemQuerier(item, selectd_server)
                        item.query_item_price()
