from config import BaseGet
from config.database import mongo

__all__ = ['GoodCollect', 'StoreCollect', 'GetGoodStatus', 'RemoveGoodCollect',
           'RemoveStoreCollect']

# 收藏相关


class GetCollect(BaseGet):
    # 获取收藏记录
    collect_set = 'user_info'
    static_set = 'goodStaticDetail'
    dynamic_set = 'goodDynamicDetail'
    store_set = 'merchant'

    @classmethod
    def _data_deal(cls, args, user):
        phone = user['phoneNum']
        type = args['type']
        page = int(args['page'])
        count = int(args['count'])
        data = {
            'good': [],
            'store': []
        }
        user_info = mongo[cls.collect_set].find_one({'phoneNum': phone})
        if user_info:
            if type == 'good':
                good_ids = user_info['collect_goods']
                good_ids.reverse()
                for id in good_ids[(page - 1) * count: page * count]:
                    try:
                        good = cls.__get_good(id)
                        if good:
                            data['good'].append(good)
                    except:
                        pass
            elif type == 'store':
                store_ids = user_info['collect_store']
                store_ids.reverse()
                for id in store_ids[(page - 1) * count: page * count]:
                    store = cls.__get_store(id)
                    if store:
                        data['store'].append(store)
        return data

    @classmethod
    def __get_good(cls, id):
        static = mongo[cls.static_set].find_one({'item_id': id},
                                                {'image_url_set': 1, 'short_name': 1, 'guonei_baoyou': 1})
        dynamic = mongo[cls.dynamic_set].find_one({'item_id': id}, {'jumei_price': 1})

        good = {
            'id': id,
            'name': static['short_name'],
            'text': static['guonei_baoyou'],
            'img': static['image_url_set']['single_many'][0]['800'],
            'price': dynamic['jumei_price']
        }
        return good

    @classmethod
    def __get_store(cls, id):
        merchant = mongo[cls.store_set].find_one({'store_id': id})
        if merchant:
            store = {
                'id': id,
                'name': merchant['name'],
                'logo': merchant['logo'],
                'collect': merchant['collection'],
                'certification': merchant['certification']
            }
            return store


class GetGoodStatus(BaseGet):
    # 获取商品收藏状态
    collect_set = 'user_info'

    @classmethod
    def _data_deal(cls, args, user):
        # 数据处理类，需重写
        phone = user['phoneNum']
        good_id = args['good_id']
        data = {
            'collect': 0,
            'wish': 0
        }
        user_info = mongo[cls.collect_set].find_one({'phoneNum': phone}, {'collect_goods': 1})
        if user_info:
            if good_id in user_info['collect_goods']:
                data['collect'] = 1
        return data


class GetStoreStatus(BaseGet):
    # 获取店铺收藏状态
    collect_set = 'user_info'

    @classmethod
    def _data_deal(cls, args, user):
        # 数据处理类，需重写
        phone = user['phoneNum']
        store_id = args['store_id']
        data = {
            'collect': 0
        }
        user_info = mongo[cls.collect_set].find_one({'phoneNum': phone}, {'collect_store': 1})
        if user_info:
            if store_id in user_info['collect_store']:
                data['collect'] = 1
        return data


class GoodCollect(BaseGet):
    # 收藏商品
    collect_set = 'user_info'

    @classmethod
    def _data_deal(cls, args, user):
        phone = user['phoneNum']
        good_id = args['good_id']
        user_info = mongo[cls.collect_set].find_one({'phoneNum': phone})
        if user_info:
            collect_goods = user_info['collect_goods']
            if good_id not in collect_goods:
                collect_goods.append(good_id)
            user_info['collect_goods'] = collect_goods
            mongo[cls.collect_set].update({'phoneNum': phone}, user_info)
            return '1'
        else:
            return '0'


class StoreCollect(BaseGet):
    # 收藏店铺
    collect_set = 'user_info'
    store_set = 'merchant'

    @classmethod
    def _data_deal(cls, args, user):
        phone = user['phoneNum']
        store_id = args['store_id']
        user_info = mongo[cls.collect_set].find_one({'phoneNum': phone})
        if user_info:
            collect_store = user_info['collect_store']
            if store_id not in collect_store:
                collect_store.append(store_id)
            user_info['collect_store'] = collect_store
            mongo[cls.collect_set].update({'phoneNum': phone}, user_info)
            store = mongo[cls.store_set].find_one({'store_id': store_id})
            if store:
                store['collection'] = str(int(store['collection']) + 1)
                mongo[cls.store_set].update({'store_id': store_id}, store)
            return '1'
        else:
            return '0'


class RemoveGoodCollect(BaseGet):
    # 取消收藏商品
    collect_set = 'user_info'

    @classmethod
    def _data_deal(cls, args, user):
        phone = user['phoneNum']
        good_id = args['good_id']
        user_info = mongo[cls.collect_set].find_one({'phoneNum': phone})
        if user_info:
            collect_goods = user_info['collect_goods']
            if good_id in collect_goods:
                collect_goods.remove(good_id)
            user_info['collect_goods'] = collect_goods
            mongo[cls.collect_set].update({'phoneNum': phone}, user_info)
            return '1'
        else:
            return '0'


class RemoveStoreCollect(BaseGet):
    # 取消收藏店铺
    collect_set = 'user_info'
    store_set = 'merchant'

    @classmethod
    def _data_deal(cls, args, user):
        phone = user['phoneNum']
        store_id = args['store_id']
        user_info = mongo[cls.collect_set].find_one({'phoneNum': phone})
        if user_info:
            collect_store = user_info['collect_store']
            if store_id in collect_store:
                collect_store.remove(store_id)
            user_info['collect_store'] = collect_store
            mongo[cls.collect_set].update({'phoneNum': phone}, user_info)
            store = mongo[cls.store_set].find_one({'store_id': store_id})
            if store:
                store['collection'] = str(int(store['collection']) - 1)
                mongo[cls.store_set].update({'store_id': store_id}, store)
            return '1'
        else:
            return '0'
