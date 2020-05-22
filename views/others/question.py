
from config import BaseServer
from config.database import mongo

__all__ = ['GetQuestionPage', 'GetQuestionAnswer', 'GetQuestionList']

# 客服中心相关


class GetQuestionPage(BaseServer):
    # 获取客服中心首页
    collect_set = 'qas'

    @classmethod
    def _data_deal(cls, args):
        data = dict(mongo[cls.collect_set].find_one({'id': "top"}))
        del data['_id']
        return data


class GetQuestionList(BaseServer):
    # 获取客服中心问题列表
    collect_set = 'qas'

    @classmethod
    def _data_deal(cls, args):
        id = args['id']
        data = dict(mongo[cls.collect_set].find_one({'id': id, 'type': 'list'}))
        del data['_id']
        return data


class GetQuestionAnswer(BaseServer):
    # 获取客服中心问题详情
    collect_set = 'qas'

    @classmethod
    def _data_deal(cls, args):
        id = args['id']
        data = dict(mongo[cls.collect_set].find_one({'id': id, 'type': 'detail'}))
        del data['_id']
        return data