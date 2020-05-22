import time

from config import r
from config.base import BaseGet, BasePost
from config.database import mongo, db
from models import Order

__all__ = ['GetPaymethod']


class GetPaymethod(BaseGet):
    # 查询支付方式
    collect_set = 'paymethod'

    @classmethod
    def _data_deal(cls, args, user):
        oid = args['oid']
        order = Order.query.filter(Order.oid == oid).first()
        if order:
            total_price = order.total_price
        else:
            total_price = 0
        method_data = mongo[cls.collect_set].find()[0]
        del method_data["_id"]
        data = {
            'total_price': total_price,
            'paymethod': method_data
        }
        return data


class Payment(BasePost):
    # 支付订单
    collect_set = 'paymethod'

    @classmethod
    def _data_deal(cls, args, user):
        oid = args['oid']
        price = args['price']
        method = args['paymethod']
        if method and price:
            order = Order.query.filter(Order.oid == oid).first()
            if order.status == 1:
                order.paymethod = method
                order.actual_price = price
                order.paytime = int(time.time())
                order.change_time = int(time.time())
                order.status = 2
                db.session.add(order)
                db.session.commit()
                cls.__set_cache(oid)
                return '1'
            else:
                return '0'
        else:
            return '0'

    @classmethod
    def __set_cache(cls, oid):
        key = 'order:delivey:' + oid
        r.set(key, int(time.time()))
        r.expire(key, 10)