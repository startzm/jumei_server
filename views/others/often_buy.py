from config import BaseGet
from config.database import mongo
from models import User

__all__ = ['OftenBuy']


class OftenBuy(BaseGet):
    static_set = 'goodStaticDetail'
    dynamic_set = 'goodDynamicDetail'

    @classmethod
    def _data_deal(cls, args, user):
        page = int(args['page'])
        count = int(args['count'])
        data = []

        user = User.query.filter(User.phoneNum == user['phoneNum']).first()
        if user:
            orders = list(user.order_of_user)[(page - 1) * count: page * count]
            for order in orders:
                item_data = {}
                good_id = order.good_id
                static = mongo[cls.static_set].find_one({'item_id': good_id},
                                                        {'image_url_set': 1, 'short_name': 1, '_id': 1})
                dynamic = mongo[cls.dynamic_set].find_one({'item_id': good_id},
                                                          {'jumei_price': 1, 'market_price': 1, 'buyer_number_text': 1})
                if static and dynamic:
                    item_data['image'] = static['image_url_set']['single_many'][0]['800']
                    item_data['name'] = static['short_name']
                    item_data['discounted_price'] = dynamic['jumei_price']
                    item_data['original_price'] = dynamic['market_price']
                    item_data['buyer_numer'] = dynamic['buyer_number_text']
                    item_data['buy_time'] = order.create_time
                    data.append(item_data)
        return {'data': data}
