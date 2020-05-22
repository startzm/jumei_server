import time

from config import BaseGet
from config.database import mongo

__all__ = ['GetWish', 'GoodWish', 'RemoveWish']

# 心愿单相关，用户指定商品和预期价格，如果商品价格降到预期以下，给用户推送降价消息


class GetWish(BaseGet):
    # 获取心愿商品
    collect_set = 'user_info'
    static_set = 'goodStaticDetail'
    dynamic_set = 'goodDynamicDetail'

    @classmethod
    def _data_deal(cls, args, user):
        phone = user['phoneNum']
        page = int(args['page'])
        count = int(args['count'])
        data = []
        user_info = mongo[cls.collect_set].find_one({'phoneNum': phone})
        if user_info:
            wish = user_info['wish']
            for item in list(dict(wish).values())[(page - 1) * count: page * count]:
                good = cls.__get_good(item['id'])
                if good:
                    good['timestamp'] = item['time']
                    good['user_price'] = item['price']
                    data.append(good)
        return {'data': data}

    @classmethod
    def __get_good(cls, id):
        static = mongo[cls.static_set].find_one({'item_id': id},
                                                {'image_url_set': 1, 'short_name': 1})
        dynamic = mongo[cls.dynamic_set].find_one({'item_id': id}, {'jumei_price': 1})

        good = {
            'id': id,
            'name': static['short_name'],
            'img': static['image_url_set']['single_many'][0]['800'],
            'price': dynamic['jumei_price']
        }
        return good


class GoodWish(BaseGet):
    # 添加心愿
    collect_set = 'user_info'

    @classmethod
    def _data_deal(cls, args, user):
        phone = user['phoneNum']
        good_id = args['good_id']
        price = float(args['price'])
        wish_item = {
            'id': good_id,
            'price': price,
            'time': int(time.time())
        }
        user_info = mongo[cls.collect_set].find_one({'phoneNum': phone})
        if user_info:
            wish = user_info['wish']
            wish[good_id] = wish_item
            user_info['wish'] = wish
            mongo[cls.collect_set].update({'phoneNum': phone}, user_info)
            return '1'
        else:
            return '0'


class RemoveWish(BaseGet):
    # 删除心愿商品
    collect_set = 'user_info'

    @classmethod
    def _data_deal(cls, args, user):
        phone = user['phoneNum']
        good_id = args['good_id']
        user_info = mongo[cls.collect_set].find_one({'phoneNum': phone})
        if user_info:
            wish = user_info['wish']
            del wish[good_id]
            user_info['wish'] = wish
            mongo[cls.collect_set].update({'phoneNum': phone}, user_info)
            return '1'
        else:
            return '0'

