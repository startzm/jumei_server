import json
from flask import request

from config import BasePost, Message
from config.database import db
from models import User

__all__ = ['Regist']


class Regist(BasePost):

    # 关闭token验证
    token_verify = False

    @classmethod
    def _data_deal(cls, args, *a):
        phoneNum = args['phoneNum']
        password = args['password']
        if User.query.filter(User.phoneNum == phoneNum).first():
            return '该号码已注册，请直接登录!'
        else:
            username = 'jumei_' + phoneNum
            new_user = User(username, phoneNum)
            db.session.add(new_user)
            db.session.commit()
            return '您已注册成功！'