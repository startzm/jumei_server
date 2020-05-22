from config import BasePost, BaseGet
from config.database import mongo, r

__all__ = ['AddCart', 'GetCart']


class AddCart(BasePost):
    # 加入购物车
    collect_set = 'cart'

    @classmethod
    def _data_deal(cls, args, user):
        phoneNum = user['phoneNum']
        item_id = args['item_id']

        cart = mongo[cls.collect_set].find_one({'phoneNum': phoneNum})
        if cart:
            if item_id in cart['cart_list']:
                cart['cart_list'][item_id]['count'] += 1
            else:
                cart['cart_list'][item_id] = {
                    'item_id': item_id,
                    'count': 1
                }
            mongo[cls.collect_set].update({'phoneNum': phoneNum}, cart)
        else:
            data = {
                'phoneNum': phoneNum,
                'cart_list': {
                    item_id: {
                        'item_id': item_id,
                        'count': 1
                    }
                }
            }
            mongo[cls.collect_set].insert(data)
        return '1'


class GetCart(BaseGet):
    # 获取购物车

    collect_set = 'cart'

    static_set = 'goodStaticDetail'
    dynamic_set = 'goodDynamicDetail'
    store_set = 'merchant'

    @classmethod
    def _data_deal(cls, args, user):
        data = []
        cart = mongo[cls.collect_set].find_one({'phoneNum': user['phoneNum']})
        if cart:
            for item in cart['cart_list']:
                try:
                    item_data = {}
                    item = cart['cart_list'][item]
                    static = mongo[cls.static_set].find_one({'item_id': item['item_id']},
                                                            {'image_url_set': 1, 'short_name': 1, 'store_id': 1,
                                                             'guonei_baoyou': 1, 'shopname': 1})
                    dynamic = mongo[cls.dynamic_set].find_one({'item_id': item['item_id']},
                                                              {'jumei_price': 1, 'market_price': 1})
                    store = mongo[cls.store_set].find_one({'store_id': static['store_id']}, {'name': 1})
                    item_data['image'] = static['image_url_set']['single_many'][0]['800']
                    item_data['name'] = static['short_name']
                    item_data['baoyou'] = static['guonei_baoyou']
                    item_data['discounted_price'] = dynamic['jumei_price']
                    item_data['original_price'] = dynamic['market_price']
                    item_data['store'] = store['name'] if store else static['shopname']
                    item_data['item_id'] = item['item_id']
                    item_data['count'] = item['count']
                    data.append(item_data)
                except:
                    pass
        data.reverse()
        return {'data_list': data}


class RemoveCart(BasePost):
    # 移除购物车
    collect_set = 'cart'

    @classmethod
    def _data_deal(cls, args, user):
        phoneNum = user['phoneNum']
        item_id = args['item_id']
        remove_all = str(args['remove_all'])
        cart = mongo[cls.collect_set].find_one({'phoneNum': phoneNum})
        if cart:
            if remove_all != '1':
                if cart['cart_list'][item_id]['count'] > 1:
                    cart['cart_list'][item_id]['count'] -= 1
                else:
                    del cart['cart_list'][item_id]
            else:
                del cart['cart_list'][item_id]
            mongo[cls.collect_set].update({'phoneNum': phoneNum}, cart)
        return '1'


class GetCartCount(BaseGet):
    # 获取购物车商品数量
    collect_set = 'cart'

    @classmethod
    def _data_deal(cls, args, user):
        phoneNum = user['phoneNum']
        cart = mongo[cls.collect_set].find_one({'phoneNum': phoneNum})
        count = 0
        if cart:
            for good in cart["cart_list"]:
                count += cart["cart_list"][good]['count']
        return {'count': count}