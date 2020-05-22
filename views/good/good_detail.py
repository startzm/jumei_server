from config import BaseServer, BaseGet
from config.database import mongo

__all__ = ['GetGoodStaticDetail', 'GetGoodDynamicDetail']


class GetGoodStaticDetail(BaseServer):
    collect_set = 'goodStaticDetail'

    @classmethod
    def _data_deal(cls, args):
        # 数据处理类，需重写
        data = {}
        good = mongo[cls.collect_set].find_one({'item_id': args['id']})
        if good:
            good['_id'] = str(good['_id'])
            data = good
        return data


class GetGoodDynamicDetail(BaseServer):
    collect_set = 'goodDynamicDetail'

    @classmethod
    def _data_deal(cls, args):
        # 数据处理类，需重写
        data = {}
        good = mongo[cls.collect_set].find_one({'item_id': args['id']})
        if good:
            good['_id'] = str(good['_id'])
            data = good
        return data
