from config import BaseGet
from views.others.integral import SetIntegral

__all__ = ['VerifyUser']


class VerifyUser(BaseGet):

    @classmethod
    def _data_deal(cls, args, user):
        data = {
            'status': 0,
            'data': {},
            'msg': ''
        }
        if user:
            SetIntegral.integral_deal(user['phoneNum'], 1, 0, cls.last_timestamp)
            data['status'] = 1
            data['data'] = user
            data['msg'] = '登录成功'
        else:
            data['msg'] = '登录已过期'

        return data
