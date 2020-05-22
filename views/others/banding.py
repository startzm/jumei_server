
from config import BaseServer
from config.database import mongo

__all__ = ['GetBanding']

# 绑定中心相关


class GetBanding(BaseServer):
    collect_set = 'banding'

    @classmethod
    def _data_deal(cls, args):
        data = dict(mongo[cls.collect_set].find_one())
        del data['_id']
        return data