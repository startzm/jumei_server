from config import BaseServer
from config.database import r

__all__ = ['GetCategoryList']


class GetCategoryList(BaseServer):

    @classmethod
    def _data_deal(cls, args):
        # 数据处理类，需重写
        data = {}
        keys = r.keys(pattern='category:*')
        for key in keys:
            k = key.split(':')[-1]
            data[k] = r.hgetall(key)
        return data