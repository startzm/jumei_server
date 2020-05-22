from config import BaseGet
from config.database import mongo

__all__ = ['GetTurntable']

# 抽奖大转盘


class GetTurntable(BaseGet):
    collect_set = 'user_info'

    @classmethod
    def _data_deal(cls, args, user):
        phone = user['phoneNum']
        user_info = mongo[cls.collect_set].find_one({'phoneNum': phone})
        if user_info:
            if user_info['sign_lottery'] >= 1:
                # 抽奖次数-1
                user_info['sign_lottery'] -= 1
                mongo[cls.collect_set].update({'phoneNum': phone}, user_info)
                return '1'
            else:
                return '0'
        else:
            return '0'
