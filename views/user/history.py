import json
import time
import re

from config import BaseGet
from config.database import r, mongo

__all__ = ['GetHistory', 'GoodHistory']


class GetHistory(BaseGet):
    # 用户浏览记录
    history_set = 'user:history'

    static_set = 'goodStaticDetail'
    dynamic_set = 'goodDynamicDetail'

    @classmethod
    def _data_deal(cls, args, user):
        data = []
        history_key = cls.history_set + ':' + user['phoneNum']
        history_list = r.lrange(history_key, 0, -1)
        for item in history_list:
            try:
                item_data = json.loads(item.replace("'", '"'))
                if item_data['good_id']:
                    item_data['timestamp'] = time.strftime("%Y-%m-%d", time.localtime(item_data['timestamp']))
                    static = mongo[cls.static_set].find_one({'item_id': item_data['good_id']},
                                                            {'image_url_set': 1, 'short_name': 1, '_id': 1})
                    dynamic = mongo[cls.dynamic_set].find_one({'item_id': item_data['good_id']},
                                                              {'jumei_price': 1, 'market_price': 1, 'buyer_number_text': 1})
                    if static and dynamic:
                        item_data['image'] = static['image_url_set']['single_many'][0]['800']
                        item_data['name'] = static['short_name']
                        item_data['discounted_price'] = dynamic['jumei_price']
                        item_data['original_price'] = dynamic['market_price']
                        item_data['buyer_numer'] = dynamic['buyer_number_text']
                        data.append(item_data)
            except:
                pass
        return {'data_list': data}


class GoodHistory(BaseGet):
    # 添加用户浏览记录
    history_set = 'user:history'

    @classmethod
    def _data_deal(cls, args, user):
        good_id = args['good_id']
        cls.__set_cache(good_id, user['phoneNum'])
        return 'success'

    @classmethod
    def __set_cache(cls, good_id, phoneNum):
        # 存入redis
        history_data = {
            'good_id': good_id,
            'timestamp': int(time.time())
        }
        history_key = cls.history_set + ':' + phoneNum
        history_list = r.lrange(history_key, 0, -1)
        for val in history_list:
            if re.findall(good_id, val):
                r.lrem(history_key, 0, val)
        r.lpush(history_key, history_data)
        if r.llen(history_key) > 60:
            # 最大可存储60条浏览记录
            r.rpop(history_key)
        # 设置过期时间为60天
        r.expire(history_key, cls.expired_time * 4)
