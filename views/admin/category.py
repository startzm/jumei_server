from config import BaseAdmin
from config.database import mongo

__all__ = ['GetCategory']


class GetCategory(BaseAdmin):
    collect_set = 'category'

    @classmethod
    def _data_deal(cls, args, admin):
        # 数据处理类，需重写
        data = []
        categories = list(mongo[cls.collect_set].find())
        if categories:
            for category in categories:
                item = {}
                children = []
                item['label'] = category['name']
                item['value'] = category['category_id']
                for child in category['sub_categories']:
                    children.append({'label': child['name'], 'value': child['category_id']})
                item['children'] = children
                data.append((item))
        return {'data': data}