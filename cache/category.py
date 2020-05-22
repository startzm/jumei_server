from config.database import r, mongo


class Category():
    # 向redis导入商品分类信息
    collect = 'category'

    @classmethod
    def _get_data(cls):
        data = {}
        category_set = mongo[cls.collect].find()
        for category in category_set:
            category['_id'] = str(category['_id'])
            data[category['_id']] = category
        return data

    @classmethod
    def set_cache(cls):
        cls._del_cache()
        category_list = cls._get_data()
        num = 0
        for category in category_list:
            r.hmset('category:' + str(num), category_list[category])
            num += 1

    @classmethod
    def _del_cache(cls):
        # 删除现有分类
        if r.keys(pattern='category:*'):
            r.delete(*r.keys(pattern='category:*'))


