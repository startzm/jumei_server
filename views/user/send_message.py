from config import BaseGet, Message

__all__ = ['SendMessage']


class SendMessage(BaseGet):

    # 关闭token验证
    token_verify = False

    @classmethod
    def _data_deal(cls, args, *a):
        phoneNum = args['phoneNum']
        data = {
            'status': 0,
            'msg': ''
        }
        status = Message.send_message(phoneNum)
        if status == 0:
            data['status'] = 1
            data['msg'] = '发送成功'
        elif status == 1:
            data['msg'] = '您输入的手机号码格式有误，请重新输入'
        elif status == 2:
            data['msg'] = '您当前操作频繁，请稍后再试'
        elif status == 3:
            data['msg'] = '抱歉，您当日验证失败次数已达上限，请于次日重试'
        return data