from flask import Blueprint

from .good_detail import GetGoodStaticDetail, GetGoodDynamicDetail
from .good_category import GetGoodCategory, GetStoreList
from .good_comment import GetGoodComment
from .good_recommend import GetGoodRecommend
from .search import GoodAjaxSearch, GoodSearch

good = Blueprint('good', __name__, url_prefix='/v1')


@good.route('/goodStaticDetail')
def get_good_static_detail():
    return GetGoodStaticDetail.get_request()


@good.route('/goodDynamicDetail')
def get_good_dynamic_detail():
    return GetGoodDynamicDetail.get_request()


@good.route('/good_category')
def get_good_category():
    return GetGoodCategory.get_request()


@good.route('/store_category')
def get_store_category():
    return GetStoreList.get_request()


@good.route('/good_comment')
def get_good_comment():
    return GetGoodComment.get_request()


@good.route('/good_recommend')
def get_good_recommend():
    return GetGoodRecommend.get_request()


@good.route('/good_search')
def good_search():
    return GoodSearch.get_request()


@good.route('/good_ajax_search')
def good_ajax_search():
    return GoodAjaxSearch.get_request()