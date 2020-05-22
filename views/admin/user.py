
from config import BaseAdmin
from models import Admin

__all__ = ['GetAdmin']


class GetAdmin(BaseAdmin):
    # 获取管理员列表

    @classmethod
    def _data_deal(cls, args, user):
        data = []
        if not user.is_super:
            return {'data': [], 'msg': '您没有权限', 'status': 0}
        else:
            query = {}
            page = int(args['page'])
            count = int(args['count'])
            for item in list(Admin.query.all())[(page-1)*count: page*count]:
                user = {}
                user['username'] = item.username
                user['id'] = item.id
                user['phoneNum'] = item.phoneNum
                user['email'] = item.email
                user['store_name'] = item.store_name
                user['store_id'] = item.store_id
                user['is_super'] = item.is_super
                data.append(user)
            return {'data': data, 'msg': '请求成功', 'status': 1, 'total': len(list(Admin.query.all()))}