from config import BaseServer
from config.database import mongo

__all__ = ['GetSubCategory']


class GetSubCategory(BaseServer):
    collect_set = 'categoryFilter'

    @classmethod
    def _data_deal(cls, args):
        # 数据处理类，需重写
        data = {}
        category_id = int(args['sub'])
        category = mongo[cls.collect_set].find_one({'category_id': category_id})
        if category:
            category['_id'] = str(category['_id'])
            data = category
        return data