import datetime
import time

from config import BaseGet, BaseServer
from config.database import mongo, r

__all__ = ['SetIntegral']

# 积分相关
# 积分获得方式
# 0 登录 1 签到 2 购物 3 分享(未实现) 4 使用 5 退回


class GetIntegral(BaseGet):
    user_info_set = 'user_info'

    @classmethod
    def _data_deal(cls, args, user):
        user_info = mongo[cls.user_info_set].find_one({'phoneNum': user['phoneNum']})
        if user_info:
            user_info['integral']['record'].reverse()
            return user_info['integral']
        else:
            return '0'


class SetIntegral():
    user_info_set = 'user_info'

    login_set = 'user:token:'
    signin_set = 'user:signin:'

    @classmethod
    def __set_integral(cls, phone, count, type):
        user_info = mongo[cls.user_info_set].find_one({'phoneNum': phone})
        integral_record = {
            'count': count,
            'type': type,
            'timestamp': int(time.time())
        }
        if user_info:
            integral = user_info['integral']
            integral['count'] += int(count)
            if len(integral['record']) > 20:
                # 最多保存20条记录
                integral['record'].pop(0)
            integral['record'].append(integral_record)
            mongo[cls.user_info_set].update({'phoneNum': phone}, user_info)
            return True

    @classmethod
    def integral_deal(cls, phone, count, type, last_timestamp=0):
        today = datetime.date.today().strftime('%Y-%m-%d')
        if type == 0 and last_timestamp != 0:
            login_time = time.strftime("%Y-%m-%d", time.localtime(int(last_timestamp)))
            if login_time != today:
                cls.__set_integral(phone, count, type)
        elif type == 1:
            signin = r.hgetall(cls.signin_set + phone)
            signin_time = time.strftime("%Y-%m-%d", time.localtime(int(signin['last_signin'])))
            if signin_time != today:
                cls.__set_integral(phone, count, type)
        else:
            cls.__set_integral(phone, count, type)


class GetIntegralRule(BaseServer):
    collect_set = 'others_rule'

    @classmethod
    def _data_deal(cls, args):
        data = mongo[cls.collect_set].find_one({'type': 'integral'})
        data['_id'] = str(data['_id'])
        return data


class GetOrderIntegral(BaseGet):
    # 查看订单是否满足使用积分条件

    collect_set = 'user_info'

    @classmethod
    def _data_deal(cls, args, user):
        price = float(args['price'])

        data = {
            'total_integral': 0,
            'discount': 0
        }

        user_info = mongo[cls.collect_set].find_one({'phoneNum': user['phoneNum']})
        if user_info:
            integral_count = user_info['integral']['count']
            data['total_integral'] = integral_count
            if integral_count > 1000:
                data['discount'] = int(integral_count / 100) if (int(integral_count / 100) < (price / 2)) else int((price / 2))
        return data
