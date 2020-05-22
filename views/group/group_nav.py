from config import BaseServer
from config.database import r

__all__ = ['GroupNav']


class GroupNav(BaseServer):

    @classmethod
    def _data_deal(cls, args):
        # 数据处理类，需重写
        data = {}
        keys = r.keys(pattern='group_category:*')
        for key in keys:
            data[key.split(':')[-1]] = r.hgetall(key)
        return data
