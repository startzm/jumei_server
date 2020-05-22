from config import BaseServer
from config.database import mongo

__all__ = ['GetStoreGoods']


class GetStoreGoods(BaseServer):
    static_set = 'goodStaticDetail'
    dynamic_set = 'goodDynamicDetail'

    @classmethod
    def _data_deal(cls, args):
        # 数据处理类，需重写
        data = {}
        sub_filter = None
        sub_category = []
        good_list = []
        query = {}

        function = args['function']
        brand = args['brand']
        sub = int(args['sub'])
        page = int(args['page'])
        count = int(args['count'])
        sort = int(args['sort'])
        min_price = float(args['min_price'])
        max_price = float(args['max_price'])
        store_id = args['store_id']

        query['store_id'] = store_id
        if min_price != 0.0:
            query['jumei_price'] = {'gte': min_price}
        if max_price != 9999.0:
            query['jumei_price'] = {'lte': max_price}
        if brand != '':
            query['brand_id'] = brand
        skip = (page - 1) * count

        if 0 < sort <= 4:
            sort_filter = cls._get_sort(sort)
            good_list = mongo[cls.static_set].find(query, {
                'short_name': 1,
                'item_id': 1,
                'image_url_set': 1}).sort(sort_filter) \
                .limit(count).skip(skip)
        else:
            good_list = mongo[cls.static_set].find(query, {
                'short_name': 1,
                'item_id': 1,
                'image_url_set': 1
            }).limit(count).skip(skip)
        for good in list(good_list):
            dynamic = mongo[cls.dynamic_set].find_one({'item_id': good['item_id']},
                                                      {'jumei_price': 1, 'market_price': 1, 'buyer_number_text': 1})
            temp = {}
            temp['image'] = good['image_url_set']['single_many'][0]['800']
            temp['name'] = good['short_name']
            temp['discounted_price'] = dynamic['jumei_price']
            temp['original_price'] = dynamic['market_price']
            temp['buyer_numer'] = dynamic['buyer_number_text']
            temp['item_id'] = good['item_id']
            temp['_id'] = str(good['_id'])
            data[temp['_id']] = temp
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
