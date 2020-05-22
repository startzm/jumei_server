import time
import random

from cache import set_cache
from config import db
from models import Order
from views.user.information import SetInformation

__all__ = ['BaseExpired', 'OrderCommentExpired', 'OrderPayExpired', 'OrderReceiveExpired',
           'GroupOrderExpired', 'RefreshExpired']


class BaseExpired():
    # 过期回调的策略类
    compiler = ''

    @classmethod
    def expired(cls, key):
        pass


class OrderPayExpired(BaseExpired):
    # 订单超时未付款取消
    compiler = '^order:pay:(.*?)'

    @classmethod
    def expired(cls, key):
        oid = key.split(':')[-1]
        order = Order.query.filter(Order.oid == oid).first()
        if order and order.status == 1:
            order.status = 6
            order.cancel_time = int(time.time())
            order.change_time = int(time.time())
            # 退款
            order.text = '未及时付款，已为您取消订单'
            db.session.commit()


class OrderReceiveExpired(BaseExpired):
    # 订单未确认收货
    compiler = '^order:received:(.*?)'

    @classmethod
    def expired(cls, key):
        oid = key.split(':')[-1]
        order = Order.query.filter(Order.oid == oid).first()
        if order and order.status == 3:
            order.status = 4
            order.cancel_time = int(time.time())
            order.change_time = int(time.time())
            order.text = '已自动收货'
            db.session.commit()


class OrderCommentExpired(BaseExpired):
    # 订单未及时评价
    compiler = '^order:comment:(.*?)'

    @classmethod
    def expired(cls, key):
        oid = key.split(':')[-1]
        order = Order.query.filter(Order.oid == oid).first()
        if order and order.status == 4:
            order.status = 5
            order.cancel_time = int(time.time())
            order.change_time = int(time.time())
            # 评价
            order.text = '已自动添加评价'
            db.session.commit()


class OrderDelivey():
    # 付款后60秒发货

    @staticmethod
    def expired(oid):
        express_id = [
            '892135971965300474', '9630184294652', '75335138905288', '75335313083706',
            '78122259015434', '4602341921231', '9861559712749'
        ]
        order = Order.query.filter(Order.oid == oid).first()
        if order and order.status == 2:
            order.status = 3
            order.delivery_time = int(time.time())
            order.change_time = int(time.time())
            order.express = random.choice(express_id)
            db.session.commit()

            SetInformation.set_information('已发货', order.good_id, oid, order.phoneNum)


class GroupOrderExpired(BaseExpired):
    compiler = '^group:(.*?)'

    @classmethod
    def expired(cls, key):
        oid = key
        order = Order.query.filter(Order.oid == oid).first()
        if order and order.status == 7:
            order.status = 5
            order.cancel_time = int(time.time())
            # 退款
            order.text = '逾期未成团，已为您退款'
            order.change_time = int(time.time())
            db.session.commit()


class RefreshExpired(BaseExpired):
    compiler = '^refresh.*?'

    @classmethod
    def expired(cls, key):
        set_cache()