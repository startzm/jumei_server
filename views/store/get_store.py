from config import BaseServer

from config.database import mongo

__all__ = ['GetStore']


class GetStore(BaseServer):
    collect_set = 'merchant'

    @classmethod
    def _data_deal(cls, args):
        # 数据处理类，需重写
        data = {}
        store_id = args['store_id']
        collect = mongo[cls.collect_set]
        data = collect.find_one({'store_id': store_id})
        if data:
            data['_id'] = str(data['_id'])
        return data
