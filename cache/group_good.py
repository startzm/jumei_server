import random

from config.database import r, mongo


class GroupGood():
    # 向redis导入首页商品信息
    collect = 'goodCategory'
    category_collect = 'category'

    @classmethod
    def _get_data(cls):
        # 每个品类下取20个商品, 每件商品随机5-8折后取整
        goods = {}
        category_list = mongo[cls.category_collect].find()
        good_set = mongo[cls.collect]
        for category in category_list:
            sub_categories = []
            for sub in category['sub_categories']:
                sub_categories.append(sub['category_id'])
            good_list = good_set.aggregate([
                {'$match': {'sub_category_id': {"$in": sub_categories}}},
                {'$sample': {'size': 20}}])
            good_list = list(good_list)
            if len(good_list) > 0:
                for good in good_list:
                    good['_id'] = str(good['_id'])
                    good['category'] = category['category_id']
                    good['group_price'] = int(good['jumei_price'] * random.randint(60, 90) / 100)
                    good['people_count'] = random.randint(50, 1000)
                    r.hmset('group_good:' + str(category['category_id']) + ":" + str(good['item_id']), good)
                del category['sub_categories']
                r.hmset('group_category:' + str(category['_id']), category)

    @classmethod
    def set_cache(cls):
        cls._del_cache()
        cls._get_data()

    @classmethod
    def _del_cache(cls):
        # 删除现有商品
        if r.keys(pattern='group_good:*'):
            r.delete(*r.keys(pattern='group_good:*'))

