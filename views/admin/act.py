
import re
from urllib import parse

from config import BaseAdmin
from config.database import db, mongo

__all__ = ['GetAct']


class GetAct(BaseAdmin):
    # 获取活动列表
    collect_set = 'act'

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
            page = int(args['page'])
            count = int(args['count'])
            q = parse.unquote(args['q'])
            if q != '':
                q_rex = re.compile('.*' + q + '.*', re.IGNORECASE)
                query['name'] = q_rex
            skip = (page - 1) * count
            act_list = mongo[cls.collect_set].find(query, {'title': 1, 'img_url': 1, 'show_title': 1, 'url': 1,
                                                           }).limit(count).skip(skip)

            for act in act_list:
                del act['_id']
                data.append(act)
            total = mongo[cls.collect_set].find(query).count()
            return {'data': data, 'msg': '请求成功', 'total': total}

