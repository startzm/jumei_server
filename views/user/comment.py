import base64
import time
import uuid
import datetime
import os
from flask import request, make_response

from config import BasePost, db
from config.database import mongo
from models import User, Order
from settings import COMMENT_PATH, IMG_PATH, COMMENT_IMG_PATH

__all__ = ['GoodComment', 'ShowCommentPhoto']


class GoodComment(BasePost):

    collect = 'goodStaticDetail'
    comment_collect = 'goodComment'

    @classmethod
    def _data_deal(cls, args, user):
        img_list = args['img_list']
        oid = args['oid']
        rate1 = args['rate1']
        rate2 = args['rate2']
        rate3 = args['rate3']
        content = args['content']

        user = User.query.filter(User.phoneNum == user['phoneNum']).first()
        order = Order.query.filter(Order.oid == oid).first()
        good = mongo[cls.collect].find_one({'item_id': order.good_id})
        if order and order.status == 4:
            imgs = []
            if img_list:
                for img_data in img_list:
                    img_data = img_data.split(',')[-1]
                    # 去掉开头的data:image/jpg:base64,
                    file_name = str(uuid.uuid4()).replace('-', '') + '.png'
                    path = COMMENT_PATH + file_name

                    with open(path, 'wb') as f:
                        f.write(base64.b64decode(img_data))
                        f.close()
                    imgs.append(COMMENT_IMG_PATH + 'file_name')

            item_id = good['item_id']
            product_id = good['product_id']

            comment_data = {
                'comment_id': str(uuid.uuid4()).replace('-', ''),
                'product_id': product_id,
                'uid': user.id,
                'face': IMG_PATH + user.header,
                'uname': user.username[0]+"***"+user.username[-1],
                'product_name': good['short_name'],
                'comments': content,
                'dateline': datetime.datetime.now().strftime('%Y-%m-%d'),
                'signature': user.slogon,
                'img_paths': imgs,
                'register_time': '',
                'like': 0,
                'reply_num': 0
            }

            comment = mongo[cls.comment_collect].find_one({'product_id': product_id})
            if comment:
                comment = dict(comment)
                comment['filterList'].append(comment_data)
                mongo[cls.comment_collect].update({'product_id': product_id}, comment)
            else:
                data = {
                    'product_id': product_id,
                    'filterList': [].append(comment_data),
                    'page_count': 1,
                    'row_count': 1,
                    'rows_per_page': 20,
                    'page_num': 1,
                    'is_show_checkall': False,
                    'rate_high': '',
                    'tag': [],
                    'item_id': item_id
                }
                mongo[cls.comment_collect].insert(data)
            order.status = 5
            order.change_time = int(time.time())
            db.session.commit()
            return '1'
        else:
            return '0'


class ShowCommentPhoto():
    @classmethod
    def get_request(cls, filename):
        if request.method == 'GET':
            if filename:
                image_data = open(os.path.join(COMMENT_PATH, '%s' % filename), "rb").read()
                response = make_response(image_data)
                response.headers['Content-Type'] = 'image/png'
                return response