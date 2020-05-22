import urllib
import re
from urllib import parse

from config import BaseAdmin, BaseServer
from config.database import db, mongo

__all__ = ['GetProduct']


class GetProduct(BaseAdmin):
    # 获取商品列表
    static_set = 'goodStaticDetail'
    dynamic_set = 'goodDynamicDetail'
    collect_set = 'goodCategory'

    @classmethod
    def _data_deal(cls, args, user):
        data = []
        if args['store_id']:
            if not user.is_super and user.store_id != args['store_id']:
                return {'data': [], 'msg': '您没有权限'}
            else:
                return ''
        else:
            query = {}
            sub = int(args['sub'] if args['sub'] else 0)
            page = int(args['page'])
            count = int(args['count'])
            q = parse.unquote(args['q'])
            min_price = float(args['min_price'])
            max_price = float(args['max_price'])
            if sub != 0:
                query['sub_category_id'] = sub
            if min_price != 0.0 or max_price != 9999.0:
                query['jumei_price'] = {
                    '$gte': min_price,
                    '$lte': max_price
                }

            if q != '':
                q_rex = re.compile('.*' + q + '.*', re.IGNORECASE)
                query['name'] = q_rex
            skip = (page - 1) * count
            good_list = mongo[cls.collect_set].find(query, {'item_id': 1, 'middle_name': 1, 'image_url_set': 1, 'jumei_price': 1,
                                                            'market_price': 1, 'product_desc': 1, 'status_num': 1}).limit(count).skip(skip)

            for good in good_list:
                good['img'] = good['image_url_set']['single']['800']
                del good['image_url_set']
                del good['_id']
                data.append(good)
            total = mongo[cls.collect_set].find(query).count()
            return {'data': data, 'msg': '请求成功', 'total': total}


class AddProduct(BaseServer):
    # 添加商品
    static_set = 'goodStaticDetail'
    dynamic_set = 'goodDynamicDetail'
    collect_set = 'goodCategory'

    @classmethod
    def _data_deal(cls, args):
        img_list = []
        description_list = ''
        for k in args:
            args[k] = urllib.parse.unquote(args[k])
        for img in args['img'].split(','):
            img_list.append({
                '800': img
            })

        for description in args['description_url_set'].split(','):
            description_list += f'<img src=\"{description}\" alt=\"\" />'

        static_info = {
            'type': args['type'],
            'item_id': args['item_id'],
            'short_name': args['short_name'],
            'name': args['name'],
            'brand_id': args['brand_id'],
            'brand_name': args['brand_name'],
            'image_url_set': {
                'dx_image': {
                    '800': args['img'].split(',')[0]
                },
                'single_many': img_list
            },
            "shopname": "本商品由 聚美优品 拥有和销售",
            'description_info': {
                'description': '',
                'description_images': description_list,
                'description_usage': "<img src=\"http://p12.jmstatic.com/global/image/201908/20/1566305182.1076.jpg\""
                                     " alt=\"\" /><img src=\"http://p12.jmstatic.com/global/image/201908/20/1566305182.5514.jpg\""
                                     " alt=\"\" />",
            }
        }

        dynamic_info = {
            'type': args['type'],
            'item_id': args['item_id'],
            'status': 'onsell' if args['status'] == 'false' else '0',
            'market_price': args['market_price'],
            'size': [],
            'brand_id': args['brand_id'],
            'guonei_baoyou': args['guonei_baoyou'],
            'jumei_price': args['jumei_price']
        }

        mongo[cls.dynamic_set].insert_one(dynamic_info)
        mongo[cls.static_set].insert_one(static_info)
        return {
            'status': 1,
            'data': {},
            'msg': '添加成功'
        }


class ChangeProduct(BaseAdmin):
    static_set = 'goodStaticDetail'
    dynamic_set = 'goodDynamicDetail'
    collect_set = 'goodCategory'

    @classmethod
    def _data_deal(cls, args, user):
        data = []
        if not user.is_super:
            return {'data': [], 'msg': '您没有权限', 'status': 0}
        else:
            static = mongo[cls.collect_set].find_one({'item_id': args['item_id']})
            if static:
                static['jumei_price'] = float(args['jumei_price'])
                mongo[cls.collect_set].update_one({'item_id': args['item_id']}, {'$set': static})
            dynamic = mongo[cls.dynamic_set].find_one({'item_id': args['item_id']})
            if dynamic:
                dynamic['jumei_price'] = args['jumei_price']
                mongo[cls.dynamic_set].update_one({'item_id': args['item_id']}, {'$set': dynamic})
            return {'data': data, 'msg': '修改成功', 'status': 1}