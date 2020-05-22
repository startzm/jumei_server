import json
import traceback
import requests

from settings import MESSAGE_USER, MESSAGE_PASSWORD, MESSAGE_URL
from config.message import smsmessage
from config.message.smsexception import *


# 文本短信发送客户端


class SmsClient():
    def __init__(self):
        self._userid = MESSAGE_USER
        self._pwd = MESSAGE_PASSWORD
        self._url = MESSAGE_URL

    @property
    def userid(self):
        return self._userid

    @property
    def pwd(self):
        return self._pwd

    @property
    def url(self):
        return self._url

    # http post
    def postSmsMessage(self, message):
        fullurl = self.url + message.apiname
        try:
            r = None
            body = message.toJson()
            timeout = (5, 30)

            headers = {'Content-Type': 'application/json', 'Connection': 'Close'}
            # 短连接请求
            r = requests.post(fullurl, data=body, headers=headers, timeout=timeout)

            r.encoding = 'utf-8'
            debugStr = '\n[------------------------------------------------------------\n' + \
                       'http url:' + fullurl + '\n' + \
                       'headers:' + headers.__str__() + '\n' + \
                       body + '\n' + \
                       'status code:' + str(r.status_code) + '\n' + \
                       r.text + \
                       '\n-------------------------------------------------------------]\n'

            # http请求失败
            if (r.status_code != requests.codes.ok):
                return message.makeupRet(SmsErrorCode.ERROR_310099)

            # 请求成功,解析服务器返回的json数据,
            rTest = json.loads(r.text)
            return rTest
        except SmsValueError as v:
            return message.makeupRet(v.errorcode)
        except requests.RequestException as e:
            print(traceback.format_exc().__str__())
            return message.makeupRet(SmsErrorCode.ERROR_310099)
        except Exception as e:
            print(traceback.format_exc().__str__())
            return message.makeupRet(SmsErrorCode.ERROR_310099)

    # 单条发送(短信)
    def singleSend(self, phone, code):
        message = smsmessage.SmsSingleMessage()
        # 发送者帐号
        message.userid = self.userid
        # 密码
        message.pwd = self.pwd
        # 接收方手机号码
        message.mobile = str(phone)
        # 验证码数字<=6位
        message.content = u'您的验证码是' + str(code) + u'，在10分钟内输入有效。如非本人操作请忽略此短信。'
        # 业务类型
        message.svrtype = ''
        # 扩展号
        message.exno = ''
        # 用户自定义流水编号：该条短信在您业务系统内的ID，比如订单号或者短信发送记录的流水号。填写后发送状态返回值内将包含这个ID。
        # 最大可支持64位的ASCII字符串：字母、数字、下划线、减号，如不需要则不用提交此字段或填空
        message.custid = ''
        # 业务类型：最大可支持10个长度的ASCII字符串：字母，数字
        message.exdata = ''

        ret = self.postSmsMessage(message)
