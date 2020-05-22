from config import BaseServer

from config.database import mongo

__all__ = ['HomeNav']


class HomeNav(BaseServer):
    collect_set = 'homeNav'

    @classmethod
    def _data_deal(cls, args):
        # 数据处理类，需重写
        data = {}
        collect = mongo[cls.collect_set]
        data = collect.find()[0]['data']
        return data
