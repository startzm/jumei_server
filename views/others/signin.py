import datetime
import time
import uuid

from config import BaseGet
from config.database import r, mongo
from .integral import SetIntegral

__all__ = ['Signin']


class Signin(BaseGet):
    # 用户每日签到
    signin_set = 'user:signin'
    user_info_set = 'user_info'
    collect_set = 'signin'


    @classmethod
    def _data_deal(cls, args, user):
        phoneNum = user['phoneNum']
        signin = r.hgetall(cls.signin_set + ":" + phoneNum)
        days = 0
        prize_data = ''
        today_checked = 0
        if signin:
            last_signin = time.strftime("%Y-%m-%d", time.localtime(int(signin['last_signin'])))
            today = datetime.date.today().strftime('%Y-%m-%d')
            if today == last_signin:
                days = int(signin['days'])
                today_checked = 1
            else:
                SetIntegral.integral_deal(phoneNum, 1, 1)
                cls.__signin(phoneNum, int(signin['days']) + 1)
                days = int(signin['days']) + 1
                if days == 7:
                    cls.__provide_coupon(phoneNum)
                    prize_data = "您已获得10元代金券，请在我的-代金券页面查看"
                if 1 <= days <= 4:
                    cls.__get_turntable(phoneNum)
                if days == 5 or days == 6:
                    cls.__get_turntable(phoneNum, 2)
        else:
            cls.__signin(phoneNum, 1)
            days = 1

        page_data = mongo[cls.collect_set].find()[0]
        del page_data["_id"]
        page_data['days'] = days
        page_data['today_checked'] = today_checked
        page_data['prize_data'] = prize_data
        page_data['turntable_count'] = mongo[cls.user_info_set].find_one({'phoneNum': phoneNum})['sign_lottery']
        return page_data

    @classmethod
    def __signin(cls, phone, days):
        data = {
            "phoneNum": phone,
            "days": days,
            "last_signin": int(time.time())
        }
        key = cls.signin_set + ":" + phone
        r.hmset(key, data)
        # 设置第三天0点过期/断签
        if days == 7:
            expried_days = 1
        else :
            expried_days = 2
        tomorrow = datetime.date.today() + datetime.timedelta(days=expried_days)
        expired_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day,
                                         0, 0, 0)
        r.expireat(key, expired_time)


    @classmethod
    def __provide_coupon(cls, phone):
        # 签到达到7天，发放10元代金券，获得3天后未使用过期删除
        coupon_id = str(uuid.uuid4()).replace('-', '')
        coupon = {
            'id': coupon_id,
            'count': 10,
            'type': 1,
            'status': 0,
            'used_order': '',
            'get_time': int(time.time()),
            'used_time': '',
            'expired_time': int(time.time()) + 259200,
            'name': '10元优惠券(签到专享)',
            'origin': '每日签到',
            'info': '所有商品(除团购、秒杀商品)可用',
            'rule': '满10元使用'
        }
        user_info = mongo[cls.user_info_set].find_one({'phoneNum': phone})
        user_info['coupons'][coupon_id] = coupon
        mongo[cls.user_info_set].update({'phoneNum': phone}, user_info)

    @classmethod
    def __get_turntable(cls, phone, count=1):
        # 签到达到1-6天，赠送抽奖转盘次数
        user_info = mongo[cls.user_info_set].find_one({'phoneNum': phone})
        if user_info:
            user_info['sign_lottery'] += count
            mongo[cls.user_info_set].update({'phoneNum': phone}, user_info)






