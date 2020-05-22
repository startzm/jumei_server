from urllib.parse import unquote

from config import BaseServer
from config.database import mongo

__all__ = ['GetAct', 'GetActPage']


class GetAct(BaseServer):
    collect_set = 'act'

    @classmethod
    def _data_deal(cls, args):
        # 数据处理类，需重写
        data = {}
        id = unquote(args['id'])
        collect = mongo[cls.collect_set]
        data = collect.find_one({'url': id})
        if data:
            data['_id'] = str(data['_id'])
        return data


class GetActPage(BaseServer):
    collect_set = 'actPage'

    @classmethod
    def _data_deal(cls, args):
        data = {}
        id = args['page_id']
        collect = mongo[cls.collect_set]
        data = collect.find_one({'page_id': id})
        if data:
            data['_id'] = str(data['_id'])
        return data