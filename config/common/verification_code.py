from random import choice

__all__ = ['VerificationCode']


class VerificationCode():
    # 生成指定位数的随机数字验证码
    seeds = "1234567890"

    @classmethod
    def get_code(cls, count):
        code = []
        for i in range(count):
            code.append(choice(cls.seeds))
        return "".join(code)

