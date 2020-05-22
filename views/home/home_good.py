from config import BaseServer
from config.database import r

__all__ = ['HomeGood']


class HomeGood(BaseServer):

    @classmethod
    def _data_deal(cls, args):
        # 数据处理类，需重写
        data = {}
        page = args['page']
        if page:
            keys = r.keys(pattern='home_good:*')
            for key in keys[(int(page) - 1) * 10: int(page) * 10]:
                data[key.split(':')[1]] = r.hgetall(key)
        return data
