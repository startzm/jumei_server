import re
from urllib import parse

from config import BaseServer
from config.database import mongo

__all__ = ['GetGoodCategory', 'GetStoreList']


class GetGoodCategory(BaseServer):

    # 分类集合
    category_set = 'category'
    # 商品集合
    collect_set = 'goodCategory'

    @classmethod
    def _data_deal(cls, args):
        # 数据处理类，需重写

        # 功效没做
        data = {}
        sub_filter = None
        sub_category = []
        good_list = ''
        query = {}
        category = int(args['category'])
        function = args['function']
        brand = args['brand']
        sub = int(args['sub'] if args['sub'] else 0)
        page = int(args['page'])
        count = int(args['count'])
        sort = int(args['sort'])
        q = parse.unquote(args['q'])
        min_price = float(args['min_price'])
        max_price = float(args['max_price'])
        if sub != 0:
            query['sub_category_id'] = sub
        if min_price != 0.0 and max_price != 9999.0:
            query['jumei_price'] = {
                '$gte': min_price,
                '$lte': max_price
            }
        if brand != '':
            query['brand_id'] = brand
        if q != '':
            q_rex = re.compile('.*' + q + '.*', re.IGNORECASE)
            query['name'] = q_rex
        skip = (page - 1) * count
        if 0 < sort <= 4:
            sort_filter = cls._get_sort(sort)
            good_list = mongo[cls.collect_set].find(query, sort=sort_filter)\
                .limit(count).skip(skip)
        else:
            good_list = mongo[cls.collect_set].find(query).limit(count).skip(skip)

        for good in good_list:
            good['_id'] = str(good['_id'])
            data[good['_id']] = good
        return data

    @classmethod
    def _get_sort(cls, sort):
        '''
        根据sort进行排序映射
        0 默认排序
        1 评论数从高到底
        2 价格升序
        3 价格降序
        4 销量降序
        '''
        sub_contrast = [
            [],
            [('deal_comments_number', -1)],
            [('jumei_price', 1)],
            [('jumei_price', -1)],
            [('fake_total_sales_number', -1)]
        ]
        sort = int(sort)
        if 0 <= sort <= 4:
            return sub_contrast[sort]


class GetStoreList(BaseServer):

    # 商店集合
    collect_set = 'merchant'

    @classmethod
    def _data_deal(cls, args):
        data = []

        page = int(args['page'])
        count = int(args['count'])
        q = parse.unquote(args['q'])
        
        skip = (page - 1) * count

        if q:
            q_rex = re.compile('.*' + q + '.*', re.IGNORECASE)
            store_list = mongo[cls.collect_set].find({'name': q_rex}) \
                .limit(count).skip(skip)
        else:
            store_list = mongo[cls.collect_set].find().limit(count).skip(skip)
        for store in store_list:
            del store['_id']
            data.append(store)
        return {
            'data': data
        }
