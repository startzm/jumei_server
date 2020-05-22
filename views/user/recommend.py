import random
import json

from config import BaseGet
from config.database import mongo, r

__all__ = ['PeopleBought', 'PersonalRecommend']


class PeopleBought(BaseGet):
    # 大家还买了板块，随机推荐商品
    # 后期考虑加入redis

    collect_set = 'cart'

    category_set = 'goodCategory'

    @classmethod
    def _data_deal(cls, args, user):
        data = {}
        # 根据用户最近加车商品推荐
        good_list = []
        cart = mongo[cls.collect_set].find_one({'phoneNum': user['phoneNum']})
        cart_list = cart['cart_list'] if cart else {}
        if cart_list:
            # 通过最近加车的5件商品筛选
            cart_list = list(cart_list.keys())[-5:]
            for i in cart_list:
                temp = mongo[cls.category_set].find_one({'item_id': i})
                category = temp['sub_category_id'] if temp else 0
                if category != 0:
                    good_list = good_list + list(mongo[cls.category_set].aggregate(
                        [{"$match": {'sub_category_id': category}}, {'$sample': {'size': 5}}]))
            if len(good_list) > 10:
                # 随机取10个商品
                good_list = random.sample(good_list, 10)
            else:
                # 不足10个商品，使用首页上新商品补至10个
                home_good = r.keys(pattern='home_good:*')
                goods = random.sample(home_good, 10 - len(good_list))
                for key in goods:
                    good_list.append(r.hgetall(key))
        else:
            home_good = r.keys(pattern='home_good:*')
            goods = random.sample(home_good, 10)
            for key in goods:
                good_list.append(r.hgetall(key))
        for good in good_list:
            good['_id'] = str(good['_id']) if good['_id'] else ''
            for k in good.keys():
                if not good[k]:
                    good[k] = ''
            data[str(good['item_id'])] = good
        return data


class PersonalRecommend(BaseGet):
    # 为您推荐板块，根据最近浏览推荐商品
    history_set = 'user:history'

    category_set = 'goodCategory'

    @classmethod
    def _data_deal(cls, args, user):
        data = {}
        good_list = []
        history_key = cls.history_set + ':' + user['phoneNum']
        history_list = r.lrange(history_key, 0, 5)
        for item in history_list:
            item_id = json.loads(item.replace("'", '"'))['good_id']
            temp = mongo[cls.category_set].find_one({'item_id': item_id})
            category = temp['sub_category_id'] if temp else 0
            if category != 0:
                good_list = good_list + list(mongo[cls.category_set].aggregate(
                    [{"$match": {'sub_category_id': category}}, {'$sample': {'size': 5}}]))

        if len(good_list) > 10:
            # 随机取10个商品
            good_list = random.sample(good_list, 10)
        else:
            home_good = r.keys(pattern='home_good:*')
            goods = random.sample(home_good, 10 - len(good_list))
            for key in goods:
                good_list.append(r.hgetall(key))

        for good in good_list:
            good['_id'] = str(good['_id'])
            for k in good.keys():
                if not good[k]:
                    good[k] = ''
            data[str(good['item_id'])] = good
        return data
