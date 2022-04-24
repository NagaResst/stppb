from json import loads

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


db = pymysql.connect(
    host='192.168.10.100',
    port=4000,
    user='uupa',
    password='lingchuan',
    database='uupa',
    charset='utf8'
)

m_id = query_user_id()
# print(m_id)
i_id = query_item_in_market()
for item_id in i_id:
    item_record = ItemQuerier(item_id)
    listings = item_record.output_sell_list()
    for record in listings:
        relist = []
        if record['isCrafted'] is True:
            if record['creatorID'] in m_id or record['sellerID'] in m_id:
                if record['retainerID'] not in relist:
                    # insert_to_db(record['worldName'], record['sellerID'], record['retainerName'], record['retainerID'])
                    relist = relist.append(record['retainerID'])
