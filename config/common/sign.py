import hashlib
import time

from settings import TIMESTAMP_SUB, TIME_DIFFERENCE, SIGN_KEY

__all__ = ['SignVerify']


class SignVerify():
    '''
    签名验证模块，根据对应参数返回签名
    验证算法：用密钥拼接时间戳的第m位与第n位，组成的字符串进行md5加密
             m n需要指定，验证时将收到的签名与后端生成的签名对比，相同则通过
    时效性： 收到的时间戳若小于当前时间的p秒内，则通过
             p需要指定
    '''

    # 时间戳验证位数
    timestamp_sub = TIMESTAMP_SUB
    # 最大时间差
    time_difference = TIME_DIFFERENCE
    # 签名加密密钥
    sign_key = SIGN_KEY

    @classmethod
    def _get_sign(cls, request_timestamp):
        sign_str = cls.sign_key
        for i in cls.timestamp_sub:
            sign_str += str(request_timestamp)[i]
        m = hashlib.md5()
        b = sign_str.encode(encoding='utf-8')
        m.update(b)
        sign = m.hexdigest()
        return sign

    @classmethod
    def verify(cls, args):
        request_sign = args['sign']
        request_timestamp = args['timestamp']
        now_time = int(time.time())
        if 0 <= abs(now_time - int(request_timestamp)) < cls.time_difference:
            sign = cls._get_sign(request_timestamp)
            if sign == request_sign:
                return True
        else:
            return False

