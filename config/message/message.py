import re
import datetime
import time

from config.database import r
from config.message.smsclient import SmsClient
from config.common import VerificationCode

__all__ = ['Message']


class Message():
    # 手机验证码发送及验证类
    key_set = 'user:sms'
    smsclient = SmsClient()

    @classmethod
    def send_message(cls, phone):
        # 发送验证短信
        if re.match(r"^1[356789]\d{9}$", str(phone)):
            if cls.__wrong_count(phone):
                if cls.__code_count(phone) and cls.__last_time(phone):
                    code = VerificationCode.get_code(6)
                    # 发送短信，调用API
                    cls.smsclient.singleSend(phone, code)
                    cls.__set_redis(phone, code)
                    return 0
                else:
                    return 2
            else:
                return 3
        else:
            return 1
        # 状态码：0代表成功 1代表电话号码格式错误 2代表操作频繁 3代表当日失败次数已达上限

    @classmethod
    def verify_message(cls, phone, code):
        # 验证短信验证码是否正确
        if not cls.__wrong_count(phone):
            return 3
        else:
            code_keys = r.keys(pattern=cls.key_set + ':' + str(phone) + ':[0123456789]*')
            for key in code_keys:
                code_val = r.hgetall(key)
                if str(code) == code_val['num']:
                    r.delete(key)
                    return 0
                else:
                    code_val['wrong_count'] = str(int(code_val['wrong_count']) + 1)
                    if int(code_val['wrong_count']) >= 3:
                        r.delete(key)
                        fail_key = cls.key_set + ':' + str(phone) + ':fail_count'
                        fail_count = int(r.get(fail_key))\
                            if(r.get(fail_key)) else 0
                        r.set(fail_key, str(fail_count + 1))
                    else:
                        r.hmset(key, code_val)

    @classmethod
    def __wrong_count(cls, phone):
        # 验证失败次数是否超过最大限制，每个手机号每日最大失败次数为5次
        key = cls.key_set + ':' + str(phone) + ':' + 'fail_count'
        val = r.get(key)
        if val:
            if int(val) > 5:
                return False
            else:
                return True
        else:
            return True

    @classmethod
    def __code_count(cls, phone):
        # 验证有效验证码数量是否超过最大限制，最多有3个有效验证码同时存在
        code_count = len(r.keys(pattern=cls.key_set + ':' + str(phone) + ':[0123456789]*'))
        if code_count > 2:
            return False
        else:
            return True

    @classmethod
    def __last_time(cls, phone):
        # 验证发送时间间隔，每个号码发送时间间隔为1分钟
        code_keys = r.keys(pattern=cls.key_set + ':' + str(phone) + ':[0123456789]*')
        now = int(time.time())
        s = 1
        if code_keys:
            for key in code_keys:
                code = r.hgetall(key)
                if now - int(code['timestamp']) > 60:
                    pass
                else:
                    s = 0
        if s == 1:
            return True
        else:
            return False

    @classmethod
    def __set_redis(cls, phone, code):
        # 将验证码存入redis
        code_key = cls.key_set + ':' + str(phone) + ':' + code
        fail_count_key = cls.key_set + ':' + str(phone) + ':' + 'fail_count'
        code_data = {
            'num': code,
            'wrong_count': 0,
            'timestamp': int(time.time())
        }
        if not r.get(fail_count_key):
            r.set(fail_count_key, 0)
            # 验证失败次数第二天0点清空
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            expired_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day,
                                             0, 0, 0)
            r.expireat(fail_count_key, expired_time)
        r.hmset(code_key, code_data)
        # 验证码10分钟后过期
        r.expire(code_key, 600)
