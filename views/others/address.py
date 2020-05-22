import uuid
import time

from config import BasePost, BaseGet
from config.database import mongo

__all__ = ['AddAddress', 'GetAddress', 'RemoveAddress', 'ChangeAddress', 'GetDefaultAddress']


class AddAddress(BasePost):
    # 添加新收货地址
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
            'id': str(uuid.uuid4()).replace('-', '')
        }
        set = mongo[cls.collect_set].find_one({'phoneNum': user_phone})
        if set:
            set = dict(set)
            set['address'][address_data['id']] = address_data
            if len(set['address'].keys()) == 1:
                set['default'] = address_data['id']
            if isDefault == 1:
                set['default'] = address_data['id']
            mongo[cls.collect_set].update({'phoneNum': user_phone}, set)
            return '1'
        else:
            return '0'


class GetAddress(BaseGet):
    # 查询收货地址
    collect_set = 'user_info'

    @classmethod
    def _data_deal(cls, args, user):
        user_phone = user['phoneNum']
        data = mongo[cls.collect_set].find_one({'phoneNum': user_phone}, {'default': 1, 'address': 1})
        if data:
           data['_id'] = str(data['_id'])
        return data


class GetDefaultAddress(BaseGet):
    # 查询默认收货地址
    collect_set = 'user_info'

    @classmethod
    def _data_deal(cls, args, user):
        user_phone = user['phoneNum']
        data = {}
        user_info = mongo[cls.collect_set].find_one({'phoneNum': user_phone})
        if user_info:
           if user_info['default'] and user_info['address']:
               data = user_info['address'][user_info['default']]
        return data


class ChangeAddress(BasePost):
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


class RemoveAddress(BasePost):
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
                del set['address'][address_id]
                set['default'] = list(set['address'].keys())[0]
            else:
                del set['address'][address_id]
            mongo[cls.collect_set].update({'phoneNum': user_phone}, set)
        return '1'