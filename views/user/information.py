import time
import uuid
from copy import deepcopy

from config import BaseGet, BaseServer
from config.database import mongo

__all__ = ['SetInformation', 'GetInformation', 'GetInformationCount', 'GetInformationPage']

# 消息中心相关
# 消息种类：1 已发货 2 已签收 3 已退款 4 退款进度 5 已拒绝退款


class GetInformationPage(BaseServer):
    collect_set = 'chat'

    @classmethod
    def _data_deal(cls, args):
        data = mongo[cls.collect_set].find()[0]
        del data['_id']
        return data


class GetInformationCount(BaseGet):
    collect_set = 'user_info'
    information_set = 'information'

    @classmethod
    def _data_deal(cls, args, user):
        count = 0
        last_time = int(time.time())
        user_info = mongo[cls.collect_set].find_one({'phoneNum': user['phoneNum']}, {'info_count': 1, 'info_list': 1})
        if user_info:
            count = user_info['info_count']
            if len(user_info['info_list']) > 0:
                info = mongo[cls.information_set].find_one({'id': user_info['info_list'][-1]})
                if info:
                    last_time = info['timestamp']
        return {'count': count, 'last_time': last_time}


class SetInformation():
    set = 'user_info'
    static = 'goodStaticDetail'
    collect = 'information'

    @classmethod
    def set_information(cls, type, good_id, oid, phoneNum):
        good = mongo[cls.static].find_one({'item_id': good_id},
                                          {'image_url_set': 1, 'short_name': 1})

        information = {
            'id': str(uuid.uuid4()).replace('-', ''),
            'title': '您的订单' + type,
            'content': '您购买的' + (good['short_name'] if len(good['short_name']) < 15 else (good['short_name'][:15] + '...')) + '订单' + type,
            'oid': oid,
            'img': good['image_url_set']['single_many'][0]['800'],
            'timestamp': int(time.time()),
            'phoneNum': phoneNum,
            'is_read': '0'
        }
        mongo[cls.collect].insert(information)
        user_info = mongo[cls.set].find_one({'phoneNum': phoneNum})
        if user_info:
            user_info['info_count'] += 1
            user_info['info_list'].append(information['id'])
            mongo[cls.set].update({'phoneNum': phoneNum}, user_info)


class GetInformation(BaseGet):
    collect = 'information'
    user_collect = 'user_info'

    @classmethod
    def _data_deal(cls, args, user):
        count = 0
        data = []
        page = int(args['page'])
        limit = int(args['count'])
        user_info = mongo[cls.user_collect].find_one({'phoneNum': user['phoneNum']})
        if user_info:
            count = user_info['info_count']
            info_list = user_info['info_list']
            info_list.reverse()
            for id in info_list[(page - 1) * limit: page * limit]:
                information = mongo[cls.collect].find_one({'id': id})
                item = deepcopy(information)
                item['_id'] = str(information['_id'])
                del information['_id']
                data.append(item)
                information['is_read'] = 1
                mongo[cls.collect].update({'id': id}, information)

            # 访问一次后将未读消息清0
            user_info['info_count'] = 0
            mongo[cls.user_collect].update({'phoneNum': user['phoneNum']}, user_info)

        return {'count': count, 'data': data}
