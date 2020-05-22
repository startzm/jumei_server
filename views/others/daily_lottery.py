import time
import datetime

from config import BaseGet, BasePost
from config.database import mongo, r

__all__ = ['GetLottery']

# 每日抽奖相关


class GetLottery(BaseGet):
    collect_set = 'lottery'
    set = 'lottery:'

    @classmethod
    def _data_deal(cls, args, user):
        phoneNum = user['phoneNum']
        today = datetime.date.today()
        tomorrow = (today + datetime.timedelta(days=1)).strftime('%m-%d')
        lottery_data = mongo[cls.collect_set].find()[0]
        data = {}
        for item in lottery_data['list']:
            key = cls.set + item['id']
            if phoneNum in r.lrange(key, 0, -1):
                item['is_joined'] = 1
            else:
                item['is_joined'] = 0
            item['tip'] = '开奖时间  ' + str(tomorrow) + '  10：00自动开奖'
            data[item['id']] = item
        return {'data': data, 'total_number': lottery_data['total_number']}


class JoinLottery(BasePost):
    set = 'lottery:'
    collect_set = 'lottery'

    @classmethod
    def _data_deal(cls, args, user):
        phoneNum = user['phoneNum']
        good_id = args['id']
        key = cls.set + good_id
        if phoneNum not in r.lrange(key, 0, -1):
            lottery_data = mongo[cls.collect_set].find()[0]
            lottery_data['total_number'] += 1
            for good in range(len(lottery_data['list'])):
                if lottery_data['list'][good]['id'] == good_id:
                    number = lottery_data['list'][good]['number'] + 1
                    lottery_data['list'][good]['number'] = number
                    break
            mongo[cls.collect_set].update({'id': lottery_data['id']}, lottery_data)
            r.lpush(key, phoneNum)
            return '1'
        else:
            return '0'
