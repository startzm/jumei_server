from config import BaseServer
from config.database import mongo

__all__ = ['GetGoodComment']


class GetGoodComment(BaseServer):
    collect_set = 'goodComment'

    @classmethod
    def _data_deal(cls, args):
        # 数据处理类，需重写
        data = {}
        product_id = args['product_id']
        comment = mongo[cls.collect_set].find_one({'product_id': product_id})
        if comment:
            comment['_id'] = str(comment['_id'])
            data = comment
        return data