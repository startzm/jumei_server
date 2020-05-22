import time
import uuid
from sqlalchemy import or_

from config import BasePost, Message
from config.database import db, r, mongo
from models import User
from views.others import SetIntegral

__all__ = ['AccountLogin', 'PhoneLogin']


class AccountLogin(BasePost):
    # 手机号/帐号 + 密码登录

    # 关闭token验证
    token_verify = False

    @classmethod
    def _data_deal(cls, args, *a):
        username = args['username']
        password = args['password']
        data = {
            'status': 0,
            'user': {},
            'msg': '您的账号/密码错误或该账号不存在'
        }
        user = User.query.filter(or_(User.phoneNum == username, User.username == username,
                             User.email == username)).first()

        if user and user.password == password:
            old_token = user.token
            user.token = str(uuid.uuid4()).replace('-', '')
            db.session.commit()
            cls.set_cache(user, old_token)
            data['user'] = {
                'token': user.token,
                'username': user.username,
                'header': user.header,
                'phoneNum': user.phoneNum
            }
            data['status'] = 1
            data['msg'] = '登录成功'
        return data

    @classmethod
    def set_cache(cls, data, old_token):
        # 存入redis
        if old_token:
            # 删除旧的token
            old_token_key = cls.token_set + ':' + old_token
            r.delete(old_token_key)
            
        user = {}
        user['token'] = data.token
        user['username'] = data.username
        user['phoneNum'] = data.phoneNum
        user['email'] = data.email
        user['header'] = data.header if data.header else 'default.png'
        user['timestamp'] = int(time.time())

        key = cls.token_set + ':' + user['token']
        r.hmset(key, user)
        # 设置过期时间
        r.expire(key, cls.expired_time)


class PhoneLogin(BasePost):
    # 手机验证码登录/注册
    # 关闭token验证
    token_verify = False

    collect_set = 'user_info'

    @classmethod
    def _data_deal(cls, args, *a):
        phoneNum = args['phoneNum']
        password = args['password']
        data = {
            'status': 0,
            'user': {},
            'msg': '验证码错误'
        }
        status = Message.verify_message(phoneNum, password)
        if status == 0:
            user = User.query.filter(or_(User.phoneNum == phoneNum, User.username == phoneNum,
                                         User.email == phoneNum)).first()
            if user:
                old_token = user.token
                user.token = str(uuid.uuid4()).replace('-', '')
                AccountLogin.set_cache(user, old_token)
            else:
                username = 'jumei_' + phoneNum
                new_user = User(username, phoneNum)
                new_user.username = username
                new_user.token = str(uuid.uuid4()).replace('-', '')
                user = new_user
                db.session.add(new_user)
                user_info = {
                    'phoneNum': phoneNum,
                    'coupons': {},
                    'integral': {'count': 0, 'record': []},
                    'collect_goods': [],
                    'collect_store': [],
                    'wish': {},
                    'daily_lottery': {},
                    'sign_lottery': 0,
                    'default': '',
                    'address': {},
                    'info_count': 0,
                    'info_list': [],
                    "message_setting": [
                        [
                            {
                                "type_id": "15",
                                "type_name": "接收新消息通知",
                                "status": 1
                            }
                        ],
                        [
                            {
                                "type_id": "1",
                                "type_name": "小美通知",
                                "status": 1
                            },
                            {
                                "type_id": "2",
                                "type_name": "交易物流",
                                "status": 1
                            },
                            {
                                "type_id": "4",
                                "type_name": "收货评价",
                                "status": 1
                            },
                            {
                                "type_id": "8",
                                "type_name": "粉丝",
                                "status": 1
                            },
                            {
                                "type_id": "10",
                                "type_name": "点赞",
                                "status": 1
                            },
                            {
                                "type_id": "12",
                                "type_name": "评论",
                                "status": 1
                            }
                        ],
                        [
                            {
                                "type_id": "13",
                                "type_name": "直播通知",
                                "status": 1
                            }
                        ],
                        [
                            {
                                "type_id": "14",
                                "type_name": "开售提醒",
                                "status": 1
                            }
                        ]
                    ]
                }
                mongo[cls.collect_set].insert(user_info)
                AccountLogin.set_cache(user, '')

            db.session.commit()
            SetIntegral.integral_deal(user.phoneNum, 1, 0, cls.last_timestamp)
            data['status'] = 1
            data['user'] = {
                'token': user.token,
                'username': user.username,
                'header': user.header,
                'phoneNum': user.phoneNum
            }
            data['msg'] = '登录成功'
        elif status == 2:
            data['msg'] = '您当前操作频繁，请稍后再试'
        elif status == 3:
            data['msg'] = '抱歉，您当日验证失败次数已达上限，请于次日重试'
        return data
