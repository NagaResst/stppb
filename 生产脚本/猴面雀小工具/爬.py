from json import loads
from time import sleep

import pymysql
from requests import get


class ItemQuerier(object):
    def __init__(self, item_id):
        """
        对象初始化
        """
        self.id = item_id
        self.result = None
        self.query_item()

    def query_item(self):
        query_url = 'https://universalis.app/api/猫小胖/%s?listings=20' % self.id
        result = get(query_url)
        result = result.text.replace('null', '"None"')
        self.result = loads(result)

    def output_sell_list(self):
        return self.result['listings']

    def output_buyer(self):
        return self.result['recentHistory']


def query_item_in_market():
    query_url = 'https://universalis.app/api/marketable'
    result = get(query_url)
    result = result.text.replace('[', '').replace(']', '')
    result = result.split(',')
    return result


def query_user_id():
    c = db.cursor()
    c.execute("select user_id from mid")
    record = c.fetchall()
    re_list = []
    for i in record:
        re_list.append(i[0])
    return re_list


def insert_sell_to_db(server, userId, retainerName, retainerId, itemId):
    c = db.cursor()
    c.execute(
        "INSERT INTO sell_record ( server, userid,retainer,retainerid,item ) VALUES  ( '%s','%s','%s','%s','%s' );" % (
            server, userId, retainerName, retainerId, itemId))
    db.commit()


def insert_buy_to_db(itemId, server, timestamp):
    c = db.cursor()
    c.execute(
        "INSERT INTO buy_record ( item,server, timestamp ) VALUES  ( '%s','%s','%s' );" % (
            itemId, server, str(timestamp)))
    db.commit()


db = pymysql.connect(
    host='192.168.10.100',
    port=4000,
    user='uupa',
    password='lingchuan',
    database='uupa',
    charset='utf8'
)

m_id = query_user_id()
print("已经获取到需要匹配的对象%d个。" % len(m_id))
# print(m_id)
i_id = query_item_in_market()
print("已经获取到可查询物品的ID。")
for item_id in i_id:
    if int(item_id) >= 7064:
        try:
            item_record = ItemQuerier(item_id)
            print('正在查询物品id %s' % item_record.id)
            listings = item_record.output_sell_list()
            history = item_record.output_buyer()
        except:
            print("清单初始化失败，15秒后重新查询物品记录")
            sleep(15)
            item_record = ItemQuerier(item_id)
            print('正在查询物品id %s' % item_record.id)
            listings = item_record.output_sell_list()
            history = item_record.output_buyer()
        for record in listings:
            relist = []
            if record['isCrafted'] is True:
                if record['creatorID'] in m_id or record['sellerID'] in m_id:
                    print("已发现雇员 %s 正在售卖物品 %s" % (record['retainerName'], item_record.id))
                    if record['retainerID'] not in relist:
                        insert_sell_to_db(record['worldName'], record['sellerID'], record['retainerName'],
                                          record['retainerID'], item_record.id)
                        print('已将雇员 %s 记录到数据库中' % record['retainerName'])
                        relist = relist.append(record['retainerID'])
        for record in history:
            if record['buyerName'] == '爱丽丝铃':
                insert_buy_to_db(item_record.id, record['worldName'], record['timestamp'])
