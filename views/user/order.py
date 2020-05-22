import uuid
import time

from sqlalchemy import and_

from models import Order, User
from config import BasePost, BaseGet, r
from config.database import mongo, db

__all__ = ['CreateOrder', 'GetOrder', 'DeleteOrder', 'ChangeOrder']


# 订单状态
# -1 所有
# 0 已删除
# 1 未付款
# 2 待发货
# 3 待收货
# 4 待评价
# 5 已完成
# 6 已取消
# 7 待成团


class CreateOrder(BasePost):
    # 创建订单
    collect_set = 'goodStaticDetail'
    address_set = 'user_info'
    expired_set = 'order:pay:'

    @classmethod
    def _data_deal(cls, args, user):
        oid = str(uuid.uuid4()).replace('-', '')
        user = User.query.filter(User.phoneNum == user['phoneNum']).first()

        uid = user.id
        user_phone = str(user.phoneNum)
        good_id = args['item_id']
        count = int(args['count'])
        unit_price = float(args['unit_price'])
        total_price = float(args['total_price'])
        coupon = args['coupon']
        coupon_discount = float(args['coupon_discount'])
        integral_discount = float(args['integral_discount'])
        integral = float(args['integral'])

        create_time = int(time.time())
        status = 1
        store = mongo[cls.collect_set].find_one({'item_id': good_id})
        store_id = store['store_id'] if store else '0'
        address_list = mongo[cls.address_set].find_one({'phoneNum': user_phone})
        user_address = address_list['address'][address_list['default']]
        phoneNum = user_address['phoneNum']
        name = user_address['name']
        address = user_address['city'] + user_address['detailAdd']

        new_order = Order(oid, uid, user_phone, good_id, count, unit_price, total_price, create_time,
                          status, store_id, phoneNum, name, address)
        new_order.change_time = int(time.time())
        if coupon and coupon_discount:
            new_order = cls.__use_coupon(coupon, phoneNum, coupon_discount, new_order)
        if integral and integral_discount:
            new_order = cls.__use_integral(integral, integral_discount, phoneNum, new_order)
        db.session.add(new_order)
        db.session.commit()
        cls.__remove_cart(user_phone, good_id, count)
        cls.__set_cache(oid)
        return {
            'status': 1,
            'oid': oid
        }

    @classmethod
    def __remove_cart(cls, phoneNum, item_id, count=1):
        # 删除购物车相应商品
        cart_set = mongo['cart'].find_one({'phoneNum': phoneNum})
        if cart_set:
            if item_id in cart_set['cart_list']:
                cart_set['cart_list'][item_id]['count'] -= count
                if cart_set['cart_list'][item_id]['count'] <= 0:
                    del cart_set['cart_list'][item_id]
                mongo['cart'].update({'phoneNum': phoneNum}, cart_set)

    @classmethod
    def __set_cache(cls, oid):
        # 未支付的订单24小时后自动取消
        key = cls.expired_set + oid
        r.set(key, int(time.time()))
        r.expire(key, 24 * 60 * 60)

    @classmethod
    def __use_coupon(cls, coupon_id, phoneNum, discount, order):
        # 使用优惠券
        user_info = mongo[cls.address_set].find_one({'phoneNum': phoneNum})
        if user_info:
            if coupon_id in user_info['coupons']:
                order.coupon_name = user_info['coupons'][coupon_id]['name']
                order.text = user_info['coupons'][coupon_id]['id']
                order.total_price = round(order.total_price * discount, 2)
                user_info['coupons'][coupon_id]['status'] = 1
                user_info['coupons'][coupon_id]['used_time'] = int(time.time())
                mongo[cls.address_set].update({'phoneNum': phoneNum}, user_info)
        return order

    @classmethod
    def __use_integral(cls, integral, count, phoneNum, order):
        # 使用积分
        user_info = mongo[cls.address_set].find_one({'phoneNum': phoneNum})
        if user_info and abs((integral / 100) - count) <= 1:
            integral_count = user_info['integral']['count']
            if integral_count >= int(integral):
                # 剩余积分大于使用积分

                if count >= order.total_price:
                    integral = int(order.total_price) * 100
                    count = int(order.total_price)

                integral_record = {
                    'count': int(integral),
                    'type': 4,
                    'timestamp': int(time.time())
                }
                user_info['integral']['count'] = int(user_info['integral']['count'] - integral)
                if len(user_info['integral']['record']) > 20:
                    # 最多保存20条记录
                    user_info['integral']['record'].pop(0)
                user_info['integral']['record'].append(integral_record)
                mongo[cls.address_set].update({'phoneNum': phoneNum}, user_info)
                order.integral_count = integral
                order.integral_discount = count

        return order


class GetOrder(BaseGet):
    # 查询订单
    collect_set = 'goodStaticDetail'
    pay_expired_set = 'order:pay:'
    received_expired_set = 'order:received:'

    @classmethod
    def _data_deal(cls, args, user):
        user_phone = user['phoneNum']
        data = []
        page = int(args['page'])
        count = int(args['count'])
        type = int(args['type'])
        order_list = []
        if type == -1:
            user = User.query.filter(User.phoneNum == user['phoneNum']).first()
            order_list = list(user.order_of_user)
        else:
            order_list = list(Order.query.filter(and_(Order.phoneNum == user['phoneNum'], Order.status == type)).all())

        for order in order_list[(page - 1) * count: page * count]:
            order_data = {}
            order_data = order.to_dict()
            good_data = mongo[cls.collect_set].find_one({'item_id': order.good_id},
                                                    {'image_url_set': 1, 'short_name': 1, 'store_id': 1,
                                                     'guonei_baoyou': 1, 'shopname': 1})
            if order.status == 1:
                pay_expire_time = r.ttl(cls.pay_expired_set + order.oid)
                order_data['pay_expire_time'] = pay_expire_time
            order_data['good_img'] = good_data['image_url_set']['single_many'][0]['800']
            order_data['good_name'] = good_data['short_name']
            order_data['good_baoyou'] = good_data['guonei_baoyou']
            order_data['good_shopname'] = good_data['shopname']
            order_data['store_id'] = good_data['store_id']
            data.append(order_data)
        return {
            'data': data
        }


class ChangeOrder(BasePost):
    # 修改收货地址
    collect_set = 'user_info'

    @classmethod
    def _data_deal(cls, args, user):
        user_phone = user['phoneNum']
        isDefault = args['isDefault']
        address_data = {
            'name': args['name'],
            'phoneNum': args['phoneNum'],
            'city': args['city'],
            'detailAdd': args['detailAdd'],
            'timestamp': int(time.time()),
            'id': args['id']
        }
        set = mongo[cls.collect_set].find_one({'phoneNum': user_phone})
        if set:
            set = dict(set)
            set['address'][address_data['id']] = address_data
            if isDefault == 1:
                set['default'] = address_data['id']
            mongo[cls.collect_set].update({'phoneNum': user_phone}, set)
        return '1'


class DeleteOrder(BasePost):
    # 删除收货地址
    collect_set = 'user_info'

    @classmethod
    def _data_deal(cls, args, user):
        user_phone = user['phoneNum']
        address_id = args['id']
        set = mongo[cls.collect_set].find_one({'phoneNum': user_phone})
        if set:
            set = dict(set)
            if set['default'] == address_id:
                set['default'] = list(set['address'].keys())[0]
            del set['address'][address_id]
            mongo[cls.collect_set].update({'phoneNum': user_phone}, set)
        return '1'


class GetOrderInfo(BasePost):
    # 获取订单信息: 收货地址、商品信息等
    address_set = 'user_info'
    cart_set = 'cart'
    static_set = 'goodStaticDetail'
    dynamic_set = 'goodDynamicDetail'
    store_set = 'merchant'

    @classmethod
    def _data_deal(cls, args, user):
        user_phone = user['phoneNum']
        good_list = args['good_list'].split(',')
        cart_goods = []
        order_goods = {}
        address = {}
        user_cart = mongo[cls.cart_set].find_one({'phoneNum': user_phone})
        user_address = mongo[cls.address_set].find_one({'phoneNum': user_phone})

        if user_address and user_address['default']:
            address = user_address['address'][user_address['default']]

            if user_cart:
                for good_id in good_list:
                    for item in user_cart['cart_list']:
                        item_data = {}
                        if good_id == user_cart['cart_list'][item]['item_id']:
                            item_data['item_id'] = good_id
                            item_data['count'] = user_cart['cart_list'][item]['count']
                            cart_goods.append(item_data)
            for good in cart_goods:
                item_data = {}
                static = mongo[cls.static_set].find_one({'item_id': good['item_id']},
                                                        {'image_url_set': 1, 'short_name': 1, 'store_id': 1,
                                                         'guonei_baoyou': 1, 'shopname': 1})
                dynamic = mongo[cls.dynamic_set].find_one({'item_id': good['item_id']},
                                                          {'jumei_price': 1})
                store = mongo[cls.store_set].find_one({'store_id': static['store_id']}, {'name': 1})
                item_data['image'] = static['image_url_set']['single_many'][0]['800']
                item_data['name'] = static['short_name']
                item_data['baoyou'] = static['guonei_baoyou']
                item_data['discounted_price'] = dynamic['jumei_price']
                item_data['store'] = store['name'] if store else static['shopname']
                item_data['item_id'] = good['item_id']
                item_data['count'] = good['count']
                order_goods[good['item_id']] = item_data
            return {
                'address': address,
                'goods': order_goods
            }
        else:
            return '0'
