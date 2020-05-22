import time
import datetime

from config import r
from .category import Category
from .home_good import HomeGood
from .home_act import HomeAct
from .group_good import GroupGood
from .mine import Mine
from .daily_lottery import DailyLottery


def set_cache():
    Category.set_cache()
    HomeGood.set_cache()
    HomeAct.set_cache()
    GroupGood.set_cache()
    Mine.set_cache()
    DailyLottery.set_cache()

    # 每天10点刷新
    key = 'refresh'
    r.set(key, int(time.time()))
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
