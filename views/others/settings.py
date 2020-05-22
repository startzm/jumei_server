import base64
import uuid

from config import BaseServer, BasePost, Message, db, BaseGet
from config.database import mongo, r
from settings import HEAD_PATH
from models import User

__all__ = ['GetRules', 'ChangeInfo', 'ChangePwd', 'MessageSettings', 'ChangeMessageSettings']

# 设置相关


class GetRules(BaseServer):
    # 获取规则
    collect_set = 'rule'

    @classmethod
    def _data_deal(cls, args):
        data = dict(mongo[cls.collect_set].find()[0])
        del data['_id']
        return data


class ChangePwd(BasePost):
    token_verify = False

    @classmethod
    def _data_deal(cls, args, *a):
        phone = args['phoneNum']
        code = args['code']
        password = args['password']
        data = {
            'status': 0,
            'msg': ''
        }
        status = Message.verify_message(phone, code)
        if status == 0:
            user = User.query.filter(User.phoneNum == phone).first()
            if user:
                user.password = password
                db.session.commit()
                data['msg'] = '修改成功'
                data['status'] = 1
            else:
                data['msg'] = '没有找到该用户，请检查号码后重试'
        else:
            data['msg'] = '验证码错误, 请重试'
        return data


class UploadHeader(BasePost):
    # 上传头像
    set = 'user:token:'

    @classmethod
    def _data_deal(cls, args, user):
        img_data = args['img']
        if img_data:
            img_data = img_data.split(',')[-1]
            # 去掉开头的data:image/jpg:base64,
            file_name = str(uuid.uuid4()).replace('-', '') + '.png'
            path = HEAD_PATH + file_name

            with open(path, 'wb') as f:
                f.write(base64.b64decode(img_data))
                f.close()

            user = User.query.filter(User.phoneNum == user['phoneNum']).first()
            user.header = file_name
            db.session.commit()
            cls.__set_cache(file_name, user.token)
            return file_name

    @classmethod
    def __set_cache(cls, path, token):
        key = cls.set + token
        user = r.hgetall(key)
        if user:
            user['header'] = path
            r.hmset(key, user)
            r.expire(key, 15 * 24 * 60 * 60)


class GetUserInfo(BaseGet):
    @classmethod
    def _data_deal(cls, args, user):
        user = User.query.filter(User.phoneNum == user['phoneNum']).first()
        if user:
           data = {
               'header': user.header,
               'username': user.username,
               'phoneNum': user.phoneNum,
               'gender': user.gender,
               'birthday': user.birth,
               'discount': user.discount,
               'slogon': user.slogon
           }
           return data


class ChangeInfo(BasePost):
    @classmethod
    def _data_deal(cls, args, user):
        info = {
            'username': args['username'] if 'username' in args else '',
            'gender': args['gender'] if 'gender' in args else '',
            'birth': args['birthday']if 'birthday' in args else '',
            'discount': args['discount']if 'discount' in args else '',
            'slogon': args['slogon']if 'slogon' in args else ''
        }
        user = User.query.filter(User.phoneNum == user['phoneNum']).first()
        if user:
            for i in info.keys():
                if info[i]:
                    if i == 'username':
                        user.username = info[i]
                        cls.__set_cache(user.username, user.token)
                    elif i == 'gender':
                        user.gender = info[i]
                    elif i == 'birth':
                        user.birth = info[i]
                    elif i == 'discount':
                        user.discount = info[i]
                    elif i == 'slogon':
                        user.slogon = info[i]
                    db.session.commit()
            return '1'
        else:
            return '0'

    @classmethod
    def __set_cache(cls, username, token):
        key = 'user:token:' + token
        user = r.hgetall(key)
        if user:
            user['username'] = username
            r.hmset(key, user)
            r.expire(key, 15 * 24 * 60 * 60)


class MessageSettings(BaseGet):
    # 新消息设置
    collect_set = 'user_info'

    @classmethod
    def _data_deal(cls, args, user):
        user_info = mongo[cls.collect_set].find_one({'phoneNum': user['phoneNum']})
        data = {
            'status': 0,
            'data': []
        }
        if user_info:
            data['status'] = 1
            data['data'] = user_info['message_setting']
        return data


class ChangeMessageSettings(BasePost):
    # 修改消息设置
    collect_set = 'user_info'

    @classmethod
    def _data_deal(cls, args, user):
        id = args['id']
        status = int(args['status'])
        user_info = mongo[cls.collect_set].find_one({'phoneNum': user['phoneNum']})
        if user_info:
            for temp in range(len(user_info['message_setting'])):
                for item in range(len(user_info['message_setting'][temp])):
                    if user_info['message_setting'][temp][item]['type_id'] == id:
                        user_info['message_setting'][temp][item]['status'] = status
                        mongo[cls.collect_set].update_one({'phoneNum': user['phoneNum']}, {'$set': user_info})
                        return '1'
        else:
            return '0'
