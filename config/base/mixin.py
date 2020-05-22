import time
from config.database import r

__all__ = ['BaseMixin']


class BaseMixin():

    # redis用户token集合
    token_set = 'user:token'

    # token过期时间
    expired_time = 15 * 24 * 60 * 60

    # 上次登录时间
    last_timestamp = 0
    
    @classmethod
    def verify_token(cls, token):
        # 验证token
        if token:
            token_key = cls.token_set + ':' + token
            token = r.hgetall(token_key)
            if len(token) != 0:
                # 每次访问过后重置token过期时间
                cls.last_timestamp = token['timestamp']
                token['timestamp'] = int(time.time())
                r.hmset(token_key, token)
                cls.set_expire(token_key)
                return token
        else:
            return None

    @classmethod
    def set_expire(cls, key):
        # 设置token过期时间
        r.expire(key, cls.expired_time)
