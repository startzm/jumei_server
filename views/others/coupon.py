import time
import datetime

from config import BaseGet
from config.database import mongo

__all__ = ['GetCoupon', 'GetOrderCoupon']

# 代金券相关
# 代金券状态对应
# 0 可用 1 已使用 2 已过期


class GetCoupon(BaseGet):
    collect_set = 'user_info'

    @classmethod
    def _data_deal(cls, args, user):
        phone = user['phoneNum']
        del_num = []
        data = {
            '0': [],
            '1': [],
            '2': []
        }
        user_info = mongo[cls.collect_set].find_one({'phoneNum': phone})
        if user_info:
            coupons = user_info['coupons']
            for i in coupons:
                if coupons[i]['status'] == 0:
                    # 如果已过期
                    if coupons[i]['expired_time'] < int(time.time()):
                        user_info['coupons'][i]['status'] = 2
                        data['2'].append(coupons[i])
                    else:
                        data['0'].append(coupons[i])
                elif coupons[i]['status'] == 1:
                    data['1'].append(coupons[i])
                else:
                    # 删除过期超过30天的券
                    if int(time.time()) - coupons[i]['expired_time'] > 2592000:
                        del_num.append(i)
                    else:
                        data['2'].append(coupons[i])
        for t in data:
            data[t].reverse()
        for num in del_num:
            del user_info['coupons'][num]
        mongo[cls.collect_set].update({'phoneNum': phone}, user_info)
        return data


class GetOrderCoupon(BaseGet):
    collect_set = 'user_info'

    @classmethod
    def _data_deal(cls, args, user):
        phone = user['phoneNum']
        price = float(args['price'])
        data = {
            'default': '',
            'coupon': [],
            'count': 0
        }
        user_info = mongo[cls.collect_set].find_one({'phoneNum': phone})
        if user_info:
            coupons = user_info['coupons']
            for i in coupons:
                if coupons[i]['status'] == 0:
                    if coupons[i]['expired_time'] > int(time.time()) and coupons[i]['count'] < price:
                        data['coupon'].append(coupons[i])
        count = len(data['coupon'])
        if count > 0:
            data['count'] = count
            data['coupon'].reverse()
            data['default'] = data['coupon'][0]['id']
        return data
