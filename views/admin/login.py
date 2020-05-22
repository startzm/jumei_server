import uuid
from sqlalchemy import or_

from config import BaseServer
from config.database import db
from models import Admin

__all__ = ['AdminLogin']


class AdminLogin(BaseServer):
    # 手机号/帐号 + 密码登录

    @classmethod
    def _data_deal(cls, args):
        username = args['username']
        password = args['password']
        data = {
            'status': 0,
            'admin': {},
            'msg': '您的账号/密码错误或该账号不存在'
        }

        admin = Admin.query.filter(or_(Admin.username == username, Admin.phoneNum == username)).first()
        if admin and admin.password == password:
            admin.token = str(uuid.uuid4()).replace('-', '')
            db.session.commit()
            data['user'] = {
                'token': admin.token,
                'username': admin.username,
                'header': admin.header,
                'phoneNum': admin.phoneNum,
                'is_super': admin.is_super,
                'store': admin.store_name,
                'store_id': admin.store_id
            }
            data['status'] = 1
            data['msg'] = '登录成功'
        return data



