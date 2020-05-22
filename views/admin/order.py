import time
import urllib
from urllib import parse

from config import BaseAdmin
from config.database import db, mongo
from models import Order

__all__ = ['GetOrder']


class GetOrder(BaseAdmin):
    # 获取订单列表
    good_collect = 'goodStaticDetail'
    store_collect = 'merchant'

    @classmethod
    def _data_deal(cls, args, user):
        data = []
        if not user.is_super:
            return {'data': [], 'msg': '您没有权限', 'status': 0}
        else:
            query = {}
            page = int(args['page'])
            count = int(args['count'])
            for item in list(Order.query.all())[(page-1)*count: page*count]:
                order = {}
                order['id'] = item.id
                order['user_phone'] = item.user_phone
                order['item_id'] = item.good_id
                order['count'] = item.count
                order['unit_price'] = item.unit_price
                order['total_price'] = item.total_price
                order['discount_info'] = item.discount_info
                order['create_time'] = item.create_time
                order['status'] = item.status
                order['store_id'] = item.store_id
                order['is_del'] = item.is_del
                order['name'] = item.name
                order['phoneNum'] = item.phoneNum
                order['address'] = item.address
                order['paymethod'] = item.paymethod
                order['actual_price'] = item.actual_price
                order['paytime'] = item.paytime
                order['express'] = item.express
                order['delivery_time'] = item.delivery_time
                order['group_time'] = item.group_time
                order['confirm_time'] = item.confirm_time
                order['cancel_time'] = item.cancel_time
                order['text'] = item.text
                order['is_group'] = item.is_group
                order['coupon_id'] = item.coupon_id
                order['coupon_name'] = item.coupon_name
                order['coupon_discount'] = item.coupon_discount
                order['integral_count'] = item.integral_count
                order['integral_discount'] = item.integral_discount
                good = mongo[cls.good_collect].find_one({"item_id": item.good_id})
                order['good_img'] = good['image_url_set']['single_many'][0]['800']
                order['good_name'] = good['short_name']
                data.append(order)
            return {'data': data, 'msg': '请求成功', 'status': 1, 'total': len(list(Order.query.all()))}


class ChangeOrder(BaseAdmin):
    # 修改訂單信息
    @classmethod
    def _data_deal(cls, args, user):
        data = []
        if not user.is_super:
            return {'data': [], 'msg': '您没有权限', 'status': 0}
        else:
            order = Order.query.filter(Order.oid == args['id']).first()
            if order:
                if args['express'] != 'null' and args['express'] != order.express:
                    order.express = args['express']
                    order.delivery_time = int(time.time())
                    order.status = 3
                order.name = urllib.parse.unquote(args['name'])
                order.address = urllib.parse.unquote(args['address'])
                order.phoneNum = args['phoneNum']
                db.session.commit()
                return {'data': data, 'msg': '修改成功', 'status': 1}


