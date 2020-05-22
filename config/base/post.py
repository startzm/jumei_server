import json
from flask import request

from .mixin import BaseMixin

__all__ = ['BasePost']


class BasePost(BaseMixin):
    # 处理需要验证用户信息的post请求

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
        args = json.loads(request.get_data())
        token = request.headers.get('token')
        if cls.token_verify:
            user = cls.verify_token(token)
            if user:
                # 数据处理
                data = cls._data_deal(args, user)
        else:
            data = cls._data_deal(args)
        # 返回数据
        return data
