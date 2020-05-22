import urllib
from urllib import parse

from config import BaseAdmin
from config.database import db
from models import User

__all__ = ['GetMember']


class GetMember(BaseAdmin):
    # 获取会员列表

    @classmethod
    def _data_deal(cls, args, user):
        data = []
        if not user.is_super:
            return {'data': [], 'msg': '您没有权限', 'status': 0}
        else:
            query = {}
            page = int(args['page'])
            count = int(args['count'])
            for item in list(User.query.all())[(page-1)*count: page*count]:
                user = {}
                user['username'] = item.username
                user['id'] = item.id
                user['phoneNum'] = item.phoneNum
                user['email'] = item.email
                user['gender'] = item.gender
                user['region'] = item.region
                data.append(user)
            return {'data': data, 'msg': '请求成功', 'status': 1, 'total': len(list(User.query.all()))}


class ChangeMember(BaseAdmin):
    # 修改会员信息
    @classmethod
    def _data_deal(cls, args, user):
        data = []
        if not user.is_super:
            return {'data': [], 'msg': '您没有权限', 'status': 0}
        else:
            user = User.query.filter(User.id == int(args['id'])).first()
            if user:
                user.username = urllib.parse.unquote(args['username'])
                user.phoneNum = args['phoneNum']
                user.email = urllib.parse.unquote(args['email'])
                user.region = urllib.parse.unquote(args['region'])
                user.gender = args['gender']
                db.session.commit()
                return {'data': data, 'msg': '修改成功', 'status': 1}
