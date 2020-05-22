from config import BaseServer
from config.database import mongo

__all__ = ['GetGoodRecommend']


class GetGoodRecommend(BaseServer):
    collect_set = 'goodCategory'

    @classmethod
    def _data_deal(cls, args):
        # 数据处理类，需重写
        data = {}
        item_id = args['item_id']
        page = args['page']
        count = args['count']

        item = mongo[cls.collect_set].find_one({'item_id': item_id})
        if item:
            sub = item['sub_category_id']
            for good in mongo[cls.collect_set].aggregate([{"$match": {'sub_category_id': sub}},
                                                          {'$sample': {'size': int(count)}}]):
                good['_id'] = str(good['_id'])
                data[good['_id']] = good
        return data