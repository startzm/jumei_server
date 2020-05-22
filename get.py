from flask import request

from .base import Basic
from .mixin import BaseMixin

__all__ = ['BaseGet']


class BaseGet(Basic, BaseMixin):
    # 处理需要验证用户信息的get请求

    # 是否要进行token验证，默认为True
    token_verify = True

    @classmethod
    def _data_deal(cls, args, user):
        pass

    @classmethod
    def get_request(cls):
        # 处理请求并返回数据
        data = {}

        # 参数解密
        temp = cls._from_code(dict(request.args)['a'][0])
        args = dict([x.split('=', 1) for x in temp.split('&')])
        token = request.headers.get('token')
        if cls.token_verify:
            user = cls.verify_token(token)
            if user:
                # 若没有签名或者签名验证失败
                if args['sign'] and cls.verify_sign(args):
                    # 数据处理
                    user['token'] = token
                    data = cls._data_deal(args, user)
        else:
            data = cls._data_deal(args)
        # 返回数据
        return data


