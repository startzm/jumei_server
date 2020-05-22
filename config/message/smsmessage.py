import hashlib
import json
import time
import urllib


class SmsBaseMessage():
    def __init__(self, apiName):
        self._fullurl = ''
        self._userid = ''
        self._pwd = ''
        self._apiname = apiName

    @property
    def fullurl(self):
        return self._fullurl

    @fullurl.setter
    def fullurl(self, fullurl):
        self._fullurl = fullurl

    @property
    def userid(self):
        return self._userid

    @userid.setter
    def userid(self, userid):
        self._userid = userid

    @property
    def pwd(self):
        return self._pwd

    @pwd.setter
    def pwd(self, pwd):
        self._pwd = pwd

    @property
    def apiname(self):
        return self._apiname

    def md5pwd(self, timestamp):
        # md5(userid + '00000000' + password + timestamp)
        tempPwd = self.userid.upper() + '00000000' + self.pwd + timestamp
        md5 = hashlib.md5()
        md5.update(tempPwd.encode('utf-8'))
        md5Pwd = md5.hexdigest()
        return md5Pwd

    def content2gbk(self, content):
        # gdb编码短信业务内容
        gbkcontent = content.encode(encoding='gbk')
        # python3.3:
        gbkcontent = urllib.parse.urlencode({'': gbkcontent})
        # python2.7:
        # gbkcontent = urllib.parse.urlencode({'': gbkcontent})
        gbkcontent = gbkcontent.split("=")[1]
        return gbkcontent

    def toJson(self):  # 虚函数，返回http body
        pass

    def makeupRet(self, errorCode):  # 虚函数，根据错误码构造返回值
        pass


# 文本短信包
class SmsTextMessage(SmsBaseMessage):
    def __init__(self, apiname):
        SmsBaseMessage.__init__(self, apiname)
        self._content = u''  # 文本内容,unicode明文
        self._timestamp = ''
        self._svrtype = ''
        self._exno = '',
        self._custid = ''
        self._exdata = ''

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content
        if self._content is None:
            self._content = u''

    @property
    def svrtype(self):
        return self._svrtype

    @svrtype.setter
    def svrtype(self, svrtype):
        self._svrtype = svrtype
        if self._svrtype is None:
            self._svrtype = ''

    @property
    def exno(self):
        return self._exno

    @exno.setter
    def exno(self, exno):
        self._exno = exno
        if self._exno is None:
            self._exno = ''

    @property
    def custid(self):
        return self._custid

    @custid.setter
    def custid(self, custid):
        self._custid = custid
        if self._custid is None:
            self._custid = ''

    @property
    def exdata(self):
        return self._exdata

    @exdata.setter
    def exdata(self, exdata):
        self._exdata = exdata
        if self._exdata is None:
            self._exdata = ''


# 单条文本短信发送包
class SmsSingleMessage(SmsTextMessage):
    def __init__(self):
        # 如:'http://api01.monyun.cn:7901/sms/v2/std/single_send'
        SmsBaseMessage.__init__(self, 'single_send')
        self._mobile = ''

    @property
    def mobile(self):
        return self._mobile

    @mobile.setter
    def mobile(self, mobile):
        self._mobile = mobile
        if self._mobile is None:
            self._mobile = ''

    # 根据错误码构造返回值
    def makeupRet(self, errorCode):
        assert isinstance(errorCode, int)
        ret = {
            'result': str(errorCode),
            'msgid': '0',
            'custid': ''
        }
        return ret

    # http body
    def toJson(self):
        timestamp = time.strftime("%m%d%H%M%S", time.localtime())  # MMDDHHMMSS
        md5pwd = self.md5pwd(timestamp)
        gbkcontent = self.content2gbk(self.content.strip())

        payload = {
            'userid': self.userid.upper(),
            'pwd': md5pwd,
            'mobile': self.mobile,
            'content': gbkcontent,
            'timestamp': timestamp,
            'svrtype': self.svrtype,
            'exno': self.exno,
            'custid': self.custid,
            'exdata': self.exdata
        }

        body = json.dumps(payload, sort_keys=False)
        return body


# 相同内容群发包
class SmsBatchMessage(SmsTextMessage):
    def __init__(self):
        # 如:'http://api01.monyun.cn/sms/v2/std/batch_send'
        SmsBaseMessage.__init__(self, 'batch_send')
        self._mobiles = ''

    @property
    def mobiles(self):
        return self._mobiles

    @mobiles.setter
    def mobiles(self, mobiles):
        self._mobiles = mobiles
        if self._mobiles is None:
            self._mobiles = ''

    # 根据错误码构造返回值
    def makeupRet(self, errorCode):
        assert isinstance(errorCode, int)
        ret = {
            'result': str(errorCode),
            'msgid': '0',
            'custid': ''
        }
        return ret

    # http body
    def toJson(self):
        timestamp = time.strftime("%m%d%H%M%S", time.localtime())  # MMDDHHMMSS
        md5pwd = self.md5pwd(timestamp)
        gbkcontent = self.content2gbk(self.content.strip())

        payload = {
            'userid': self.userid.upper(),
            'pwd': md5pwd,
            'mobile': self.mobiles,
            'content': gbkcontent,
            'timestamp': timestamp,
            'svrtype': self.svrtype,
            'exno': self.exno,
            'custid': self.custid,
            'exdata': self.exdata
        }

        body = json.dumps(payload, sort_keys=False)
        return body


# 个性化群发接口
class SmsMultiMessage(SmsBaseMessage):
    def __init__(self):
        SmsBaseMessage.__init__(self, 'multi_send')
        self._multimt = list()

    # 增加接收短信者
    def addReciver(self, mobile, content, svrtype, exno, custid, exdata):
        item = (mobile, content, svrtype, exno, custid, exdata)
        self._multimt.append(item)

    # 根据错误码构造返回值
    def makeupRet(self, errorCode):
        assert isinstance(errorCode, int)
        ret = {
            'result': str(errorCode),
            'msgid': '0',
            'custid': ''
        }
        return ret

    def toJson(self):
        timestamp = time.strftime("%m%d%H%M%S", time.localtime())  # MMDDHHMMSS
        md5pwd = self.md5pwd(timestamp)

        payload = {
            'userid': self.userid.upper(),
            'pwd': md5pwd,
            'timestamp': timestamp
        }

        multimt = []
        for item in self._multimt:
            mobile = item[0]
            content = item[1]
            svrtype = item[2]
            exno = item[3]
            custid = item[4]
            exdata = item[5]

            gbkcontent = self.content2gbk(content.strip())
            reciever = {
                'mobile': mobile,
                'content': gbkcontent,
                'svrtype': svrtype,
                'exno': exno,
                'custid': custid,
                'exdata': exdata
            }
            multimt.append(reciever)

        payload['multimt'] = multimt
        body = json.dumps(payload, sort_keys=False)
        return body


# 获取上行包
class SmsMo(SmsBaseMessage):
    def __init__(self):
        SmsBaseMessage.__init__(self, 'get_mo')
        self._retsize = 100  # 每次请求想要获取的上行最大条数,默认100条

    @property
    def retsize(self):
        return self._retsize

    @retsize.setter
    def retsize(self, retsize):
        # 每次请求想要获取的上行最大条数。最大200,超过200按200返回。小于等于0或不填时，系统返回默认条数，默认100条
        if retsize is not None:
            assert isinstance(retsize, int)
            self._retsize = retsize
            if retsize > 200:
                self._retsize = 200
            if retsize <= 0:
                self._retsize = 100

    # 根据错误码构造返回值
    def makeupRet(self, errorCode):
        assert isinstance(errorCode, int)
        ret = {
            'result': str(errorCode),
            'mos': []
        }
        return ret

    def toJson(self):

        timestamp = time.strftime("%m%d%H%M%S", time.localtime())  # MMDDHHMMSS
        md5pwd = self.md5pwd(timestamp)

        payload = {
            'userid': self.userid.upper(),
            'pwd': md5pwd,
            'timestamp': timestamp,
            'retsize': self.retsize
        }

        body = json.dumps(payload, sort_keys=False)
        return body


# 获取状态报告接口
class SmsRpt(SmsBaseMessage):
    def __init__(self):
        SmsBaseMessage.__init__(self, 'get_rpt')
        self._retsize = 500  # 每次请求想要获取的上行最大条数,默认500条

    @property
    def retsize(self):
        return self._retsize

    @retsize.setter
    def retsize(self, retsize):
        # 每次请求想要获取的上行最大条数。最大500,超过500按500返回。小于等于0或不填时，系统返回默认条数，默认500条
        if retsize is not None:
            assert isinstance(retsize, int)
            self._retsize = retsize
            if retsize > 500:
                self._retsize = 500
            if retsize <= 0:
                self._retsize = 100

    # 根据错误码构造返回值
    def makeupRet(self, errorCode):
        assert isinstance(errorCode, int)
        ret = {
            'result': str(errorCode),
            'rpts': []
        }
        return ret

    def toJson(self):

        timestamp = time.strftime("%m%d%H%M%S", time.localtime())  # MMDDHHMMSS
        md5pwd = self.md5pwd(timestamp)

        payload = {
            'userid': self.userid.upper(),
            'pwd': md5pwd,
            'timestamp': timestamp,
            'retsize': self.retsize
        }

        body = json.dumps(payload, sort_keys=False)
        return body


# 查询余额包
class SmsBalanceMessage(SmsBaseMessage):
    def __init__(self):
        SmsBaseMessage.__init__(self, 'get_balance')

    # 根据错误码构造返回值
    def makeupRet(self, errorCode):
        assert isinstance(errorCode, int)
        ret = {
            'result': str(errorCode),
            'chargetype': '0',
            'balance': '0',
            'money': '0'
        }
        return ret

    # 组包,仅http body
    def toJson(self):
        # md5(userid + '00000000' + password + timestamp)
        timestamp = time.strftime("%m%d%H%M%S", time.localtime())  # MMDDHHMMSS
        md5pwd = self.md5pwd(timestamp)

        # http body
        payload = {
            'userid': self.userid.upper(),
            'pwd': md5pwd,
            'timestamp': timestamp,
        }

        body = json.dumps(payload, sort_keys=False)
        return body
