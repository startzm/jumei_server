# coding=utf-8
import requests
import json

from settings import EXPRESS_KEY, EXPRESS_URL

# 出现SSL错误时，安装cryptography pyOpenSSL certifi三个包


class Express():
    # 物流查询API

    url = '%(base_url)s?appkey=%(app_key)s&type=%(type)s&number=%(number)s'

    @classmethod
    def get_track(cls, number, type='auto'):
        request_url = cls.url % {
            'base_url': EXPRESS_URL,
            'app_key': EXPRESS_KEY,
            'number': number,
            'type': type
        }
        result = cls.__request_api(request_url)
        return result

    @classmethod
    def __request_api(cls, url):
        # t = '{"status":0,"msg":"ok","result":{"number":"4303200322000","type":"yunda","typename":"韵达快运","logo":"https:\/\/api.jisuapi.com\/express\/static\/images\/logo\/80\/yunda.png","list":[{"time":"2019-12-30 13:53:32","status":"山东黄岛区公司石油大学外围便民服务站快件已被 您的快件已送达  青岛瑞源名嘉汇小区店快件已暂存至青岛瑞源名嘉汇小区店菜鸟驿站如有疑问请联系13863920389 保管。如有问题请电联业务员：张仲民【13256828733】。相逢是缘,如果您对我的服务感到满意,给个五星好不好？【请在评价小件员处给予五星好评】"},{"time":"2019-12-30 12:05:01","status":"山东黄岛区公司石油大学外围便民服务站进行派件扫描；派送业务员：张仲民；联系电话：13256828733"},{"time":"2019-12-30 07:46:26","status":"山东黄岛区公司进行快件扫描，发往：山东黄岛区公司石油大学外围便民服务站"},{"time":"2019-12-29 19:35:01","status":"山东黄岛区公司到达目的地网点，快件很快进行派送"},{"time":"2019-12-29 15:47:19","status":"山东青岛分拨中心从站点发出，本次转运目的地：山东黄岛区公司"},{"time":"2019-12-29 14:40:16","status":"山东青岛分拨中心在分拨中心进行卸车扫描"},{"time":"2019-12-28 00:44:18","status":"广东广州分拨中心进行装车扫描，发往：山东青岛分拨中心"},{"time":"2019-12-28 00:42:41","status":"广东广州分拨中心在分拨中心进行称重扫描"},{"time":"2019-12-28 00:22:35","status":"广东广州白云区红星公司进行下级地点扫描，发往：山东青岛分拨中心"},{"time":"2019-12-27 21:31:57","status":"广东广州白云区红星公司进行揽件扫描"}],"deliverystatus":3,"issign":1}}'
        # t = json.loads(t)
        # return t['result']
        res = requests.get(url, verify=False)
        if res.status_code == 200:
            return json.loads(res.text)['result']
        else:
            return {}

# print(Express.get_track('73126445849214'))