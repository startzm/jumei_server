import datetime
import time
import json
import uuid

from config import BaseServer, BasePost, db
from config.database import r, mongo
from models import User, Order
from settings import IMG_PATH

__all__ = ['GroupGood', 'StartGroup']

# 团购相关
# 设计思路： 为开团者直接建立新订单，订单状态为已付款未成团，redis添加groupkey，失效时间为第二天10点
# 若groupkey过期时未成团，则触发过期回调，订单取消，为开团者退款。
# 若已成团，双方订单状态变为已成团待发货，拼团完成。


class GroupGood(BaseServer):

    @classmethod
    def _data_deal(cls, args):
        # 数据处理类，需重写
        data = {}
        group_id = args['group_id']
        page = args['page']
        count = args['count']
        if group_id:
            pattern = 'group_good:' + group_id + ':*'
        else:
            pattern = 'group_good:*'
        keys = r.keys(pattern=pattern)
        for key in keys[(int(page) - 1) * 10: int(page) * 10]:
            data[key.split(':')[-1]] = r.hgetall(key)
        return data


class GroupDetail(BaseServer):
    set = 'group_good:'
    group_info = 'group:'

    @classmethod
    def _data_deal(cls, args):
        good_id = args['good_id']
        data = {}
        group = []
        pattern = cls.set + '*:' + good_id
        good = r.hgetall(r.keys(pattern=pattern)[0])
        if good:
            keys = r.keys(pattern=cls.group_info + good_id + ':*')
            for k in keys:
                group_info = r.hgetall(k)
                group.append(group_info)
            data = {
                'group_price': good['group_price'],
                'group': group,
                'people_count': good['people_count']
            }
        return data


class StartGroup(BasePost):
    # 创建团购订单
    set = "group:"
    collect_set = 'goodStaticDetail'
    address_set = 'user_info'

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
        group_id = args['group_id']
        create_time = int(time.time())
        if cls.good_valid(good_id):
            if group_id and cls.group_valid(group_id, good_id, user_phone):
                status = 2
                is_group = True
                group_time = int(time.time())
                cls.__change_head_order(group_id, good_id)
            else:
                status = 7
                is_group = False
                group_time = 0
                cls.__set_cache(oid, user, good_id)

            store = mongo[cls.collect_set].find_one({'item_id': good_id})['store_id']
            store_id = store if store else '0'
            address_list = mongo[cls.address_set].find_one({'phoneNum': user_phone})
            user_address = address_list['address'][address_list['default']]
            phoneNum = user_address['phoneNum']
            name = user_address['name']
            address = user_address['city'] + user_address['detailAdd']

            new_order = Order(oid, uid, user_phone, good_id, count, unit_price, total_price, create_time,
                              status, store_id, phoneNum, name, address)
            new_order.is_group = is_group
            new_order.group_time = group_time
            new_order.change_time = int(time.time())
            db.session.add(new_order)
            db.session.commit()
            return {
                'status': 1,
                'oid': oid
            }
        else:
            return {
                'status': 0,
                'oid': ''
            }

    @classmethod
    def group_valid(cls, group_id, good_id, phone):
        # 验证团购订单是否合法
        group = r.hgetall(cls.set + good_id + ":" + group_id)
        if group:
            if r.keys(pattern='group_good:*' + ':' + group['good']) and group['phone'] != phone:
                return True
        else:
            return False

    @classmethod
    def good_valid(cls, good_id):
        # 验证商品是否为团购商品
        if r.keys(pattern='group_good:*' + ':' + good_id):
            return True

    @classmethod
    def __set_cache(cls, oid, user, good_id):
        if len(user.username) > 2:
            username = user.username[0] + '***' + user.username[-1]
        else:
            username = "***" + user.username[-1]
        data = {
            'phone': str(user.phoneNum)[0:3] + "****" + str(user.phoneNum)[7:],
            'header': IMG_PATH + user.header if user.header else IMG_PATH + 'default.png',
            'timestamp': int(time.time()),
            'username': username,
            'group_id': oid,
            'good': good_id
        }
        key = cls.set + good_id + ":" + oid
        r.hmset(key, data)
        hour = datetime.datetime.now().hour
        if hour >= 10:
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            expired_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day,
                                             10, 0, 0)
        else:
            today = datetime.date.today()
            expired_time = datetime.datetime(today.year, today.month, today.day,
                                             10, 0, 0)
        r.expireat(key, expired_time)

    @classmethod
    def __change_head_order(cls, oid, good_id):
        # 修改开团者订单状态
        order = Order.query.filter(Order.oid == oid).first()
        if order and order.status == 7:
            order.status = 2
            order.is_group = True
            order.group_time = int(time.time())
            order.change_time = int(time.time())
            db.session.commit()
            r.delete(cls.set + good_id + ':' + oid)
            return True
        else:
            return False

