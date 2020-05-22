from flask import request

from .base import Basic
from models import Admin

__all__ = ['BaseAdmin']


class BaseAdmin(Basic):
    # 处理管理员请求

    @classmethod
    def _data_deal(cls, args, admin):
        pass

    @classmethod
    def get_request(cls):
        # 处理请求并返回数据
        data = {}

        # 参数解密

        temp = cls._from_code(dict(request.args)['a'])
        args = dict([x.split('=', 1) for x in temp.split('&')])
        token = request.cookies.get('token')
        if token:
            admin = cls.verify_token(token)
            if admin:
                # 若没有签名或者签名验证失败
                if args['sign'] and cls.verify_sign(args):
                    # 数据处理
                    data = cls._data_deal(args, admin)
        else:
            data = {'status': '-1', 'data': {}, 'msg': '登录失效'}
        # 返回数据
        return data

    @classmethod
    def verify_token(cls, token):
        # 验证token
        if token:
            admin = Admin.query.filter(Admin.token == token).first()
            if admin:
                return admin
        else:
            return None