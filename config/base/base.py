from settings import URL_KEY
from ..common import SignVerify

__all__ = ['Basic']


class Basic():
    # 签名验证函数
    verify_sign = SignVerify.verify

    # url加密密钥
    key = URL_KEY

    @classmethod
    def get_request(cls):
        # 请求处理，需重写
       pass

    @classmethod
    def _from_code(cls, code_str):
        # 参数解密
        l = len(cls.key)
        d = 0
        s = []
        b = int(len(code_str) / 3)
        for i in range(b):
            b1 = cls.key.find(code_str[d])
            d += 1
            b2 = cls.key.find(code_str[d])
            d += 1
            b3 = cls.key.find(code_str[d])
            d += 1
            s.append(b1 * l * l + b2 * l + b3)
        s = [chr(i) for i in s]
        return ''.join(s)
