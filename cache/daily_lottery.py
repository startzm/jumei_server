import datetime

from config.database import r, mongo


class DailyLottery():
    # 每日抽奖
    collect_set = 'lottery'

    @classmethod
    def _get_data(cls):
        goods = mongo[cls.collect_set].find()[0]['list']
        return goods

    @classmethod
    def set_cache(cls):
        cls._del_cache()
        for good in cls._get_data():
            k = 'lottery:' + good['id']
            r.lpush(k, '')
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            expired_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day,
                                             10, 0, 0)
            r.expireat(k, expired_time)

    @classmethod
    def _del_cache(cls):
        # 删除现有活动
        if r.keys(pattern='lottery:*'):
            r.delete(*r.keys(pattern='lottery:*'))
