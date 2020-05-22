import os
from flask import request, make_response
from sqlalchemy import and_

from config import BaseServer, r
from config.database import mongo
from models import User, Order
from settings import HEAD_PATH

__all__ = ['GetMine', 'GetLogin', 'ShowPhoto']


class GetMine(BaseServer):
    collect_set = 'user_info'
    history_set = 'user:history'

    @classmethod
    def _data_deal(cls, args):
        # 数据处理类，需重写
        phone = args['phoneNum']
        # data = {}
        #         # keys = r.keys(pattern='mine:*')
        #         # data = r.hgetall(keys[0])
        data = mongo['mine'].find()[0]
        data['_id'] = str(data['_id'])
        # print(data)
        # temp = {}
        # for k in data.items():
        #     temp[k] = json.dumps(data[k].replace("'", "'"), ensure_ascii=False)
        if phone:
            user = User.query.filter(User.phoneNum == phone).first()
            user_info = mongo[cls.collect_set].find_one({'phoneNum': phone})
            if user_info and user:
                data['user'] = {
                    'gender': user.gender,
                    'discount': user.discount
                }

                data['panels'][0]['items']['fav_product']['dot'] = len(user_info['collect_goods'])
                data['panels'][0]['items']['fav_shoppe']['dot'] = len(user_info['collect_store'])
                data['panels'][0]['items']['viewed']['dot'] = r.llen(cls.history_set + ':' + phone)
                data['panels'][0]['items']['buy_often']['dot'] = len(list(user.order_of_user))

                data['panels'][1]['items']['wait_pay']['dot'] = len(list(Order.query.filter(and_(Order.phoneNum == phone, Order.status == 1)).all()))
                data['panels'][1]['items']['wait_send']['dot'] = len(list(Order.query.filter(and_(Order.phoneNum == phone, Order.status == 2)).all()))
                data['panels'][1]['items']['wait_confirm']['dot'] = len(list(Order.query.filter(and_(Order.phoneNum == phone, Order.status == 3)).all()))
                data['panels'][1]['items']['wait_rate']['dot'] = len(list(Order.query.filter(and_(Order.phoneNum == phone, Order.status == 4)).all()))

                data['panels'][3]['items']['promocard']['dot'] = len(list(dict(user_info['coupons']).keys()))
                data['panels'][3]['items']['jumei_point']['dot'] = user_info['integral']['count']
        return data


class GetLogin(BaseServer):

    @classmethod
    def _data_deal(cls, args):
        # 数据处理类，需重写
        data = mongo['login'].find()[0]
        data['_id'] = str(data['_id'])
        return data


class ShowPhoto():
    @classmethod
    def get_request(cls, filename):
        if request.method == 'GET':
            if filename:
                image_data = open(os.path.join(HEAD_PATH, '%s' % filename), "rb").read()
                response = make_response(image_data)
                response.headers['Content-Type'] = 'image/png'
                return response