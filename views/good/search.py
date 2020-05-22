import re
from urllib import parse

from config import BaseServer
from config.database import mongo

__all__ = ['GoodSearch', 'GoodAjaxSearch']

# 商品关键字查询


class GoodSearch(BaseServer):

    # 商品集合
    collect_set = 'goodStaticDetail'

    @classmethod
    def _data_deal(cls, args):
        data = {}
        q = args['q']
        page = int(args['page'])
        count = int(args['count'])

        skip = (page - 1) * count
        good_list = mongo[cls.collect_set].find({'name': re.compile(q)})\
            .limit(count).skip(skip)

        for good in good_list:
            good['_id'] = str(good['_id'])
            data[good['_id']] = good
        return data


class GoodAjaxSearch(BaseServer):
    # 输入关键字提示

    collect_set = 'goodStaticDetail'
    @classmethod
    def _data_deal(cls, args):
        data = []
        q = parse.unquote(args['q'])
        rexExp = re.compile('.*' + q + '.*', re.IGNORECASE)
        good_list = list(mongo[cls.collect_set].find({'name': rexExp}, {'short_name': 1}).limit(10))
        for good in good_list:
            data.append(good['short_name'])
        return {
            'data': data
        }