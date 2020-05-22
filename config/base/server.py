import json
from flask import request

from .base import Basic

__all__ = ['BaseServer']


class BaseServer(Basic):
    # 主要处理不必须要求携带用户信息的jsonp请求

    # mongo集合名
    collect_set = ''

    @classmethod
    def _data_deal(cls, args):
        # 数据处理，需重写
        pass

    @classmethod
    def get_request(cls):
        # 处理请求并返回数据
        response_data = {}
        status = 0
        data = {}
        msg = []

        # 参数解密
        temp = cls._from_code(dict(request.args)['a'][0])
        args = dict([x.split('=', 1) for x in temp.split('&')])
        # 若没有jsonp回调
        if request.args['callback']:
            # 若没有签名或者签名验证失败
            if args['sign'] and cls.verify_sign(args):
                status = 1
                # 数据处理
                data = cls._data_deal(args)
                msg = [
                    '请求成功'
                ]
            else:
                msg = [
                    '签名不正确'
                ]
        else:
            msg = [
                '请求错误'
            ]

        callback = request.args['callback'] if request.args['callback'] else 'callback'
        # 返回数据
        response_data['status'] = status
        response_data['data'] = data
        response_data['msg'] = msg
        return str(callback) + "(" + json.dumps(response_data) + ")"



