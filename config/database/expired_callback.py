import re

from ..base.expired import BaseExpired
from .redis import r

__all__ = ['ExpiredCallback']

# redis过期回调，负责处理未及时付款订单、未及时收货订单、未及时评价订单、未成功拼团订单


class ExpiredCallback():
    # pub/sub频道
    pubsub = r.pubsub()

    @classmethod
    def __event_handler(cls, data):
        key = data['data']

        for sc in BaseExpired.__subclasses__():
            if re.search(sc().compiler, key):
                sc().expired(key)

    @classmethod
    def monitor(cls):
        cls.pubsub.psubscribe(**{'__keyevent@0__:expired': cls.__event_handler})
        # 开启线程订阅过期事件
        thread = cls.pubsub.run_in_thread(sleep_time=60)
