import random
import time

from config import BaseGet, Express, BasePost, db, r
from config.database import mongo
from models import Order
from views.others import SetIntegral
from views.user.information import SetInformation

__all__ = ['OrderDetail', 'OrderReceived', 'OrderComment']


class OrderDetail(BaseGet):
    static_set = 'goodStaticDetail'

    @classmethod
    def _data_deal(cls, args, user):
        oid = args['id']
        item_data = {}

        order = Order.query.filter(Order.oid == oid).first()
        if order and order.user_phone == user['phoneNum']:
            good_id = order.good_id
            static = mongo[cls.static_set].find_one({'item_id': good_id},
                                                    {'image_url_set': 1, 'guonei_baoyou': 1,
                                                     'shopname': 1, 'short_name': 1})
            if order.status == 3 or order.status == 4:
                item_data['express'] = Express.get_track(order.express)

            item_data['image'] = static['image_url_set']['single_many'][0]['800']
            item_data['name'] = static['short_name']
            item_data['baoyou'] = static['guonei_baoyou']
            item_data['discounted_price'] = order.unit_price
            item_data['item_id'] = good_id
            item_data['create_time'] = order.create_time
            item_data['status'] = order.status
            item_data['pay_time'] = order.paytime
            item_data['count'] = order.count
            item_data['id'] = oid
            item_data['total_price'] = order.total_price
            item_data['address'] = {
                'phoneNum': order.phoneNum,
                'detailAdd': order.address,
                'city': '',
                'name': order.name
            }
            return item_data
        else:
            return {}


def change_order_status(oid, phone, status):
    order = Order.query.filter(Order.oid == oid).first()
    if order and order.phoneNum == phone:
        order.status = status
        order.change_time = int(time.time())
        db.session.commit()
        if status == 4:
            SetIntegral.integral_deal(phone, int(order.total_price), 2)
        return True
    else:
        return False


class OrderReceived(BaseGet):
    expired_set = 'order:comment:'

    @classmethod
    def _data_deal(cls, args, user):
        if change_order_status(args['id'], user['phoneNum'], 4):
            cls.__set_cache(args['id'])
            order = Order.query.filter(Order.oid == args['id']).first()
            SetInformation.set_information('已签收', order.good_id, args['id'], order.phoneNum)
            return '1'
        else:
            return '0'

    @classmethod
    def __set_cache(cls, oid):
        # 7天未评价的订单自动好评
        key = cls.expired_set + oid
        r.set(key, int(time.time()))
        r.expire(key, 7 * 24 * 60 * 60)


class OrderComment(BasePost):
    @classmethod
    def _data_deal(cls, args, user):
        if change_order_status(args['id'], user['phoneNum'], 5):
            return '1'
        else:
            return '0'


