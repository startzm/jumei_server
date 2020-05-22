from config.database import r, mongo


class HomeGood():
    # 向redis导入首页商品信息
    collect = 'goodCategory'

    @classmethod
    def _get_data(cls):
        # 随机取100个商品
        goods = {}
        good_set = mongo[cls.collect]
        for good in good_set.aggregate([{'$sample': {'size': 100}}]):
            good = dict(good)
            good['_id'] = str(good['_id'])
            goods[str(good['_id'])] = good
        return goods

    @classmethod
    def set_cache(cls):
        cls._del_cache()
        goods = cls._get_data()
        for k, v in goods.items():
            r.hmset('home_good:' + k, v)

    @classmethod
    def _del_cache(cls):
        # 删除现有商品
        if r.keys(pattern='home_good:*'):
            r.delete(*r.keys(pattern='home_good:*'))

