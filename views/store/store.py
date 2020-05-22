from flask import Blueprint

from .get_store import GetStore
from .get_store_good import GetStoreGoods
from .get_act import GetAct, GetActPage

store = Blueprint('store', __name__, url_prefix='/v3')


@store.route('/get_store')
def get_store():
    return GetStore.get_request()


@store.route('/get_store_good')
def get_store_good():
    return GetStoreGoods.get_request()


@store.route('/get_act')
def get_act():
    return GetAct.get_request()


@store.route('/get_act_page')
def get_act_page():
    return GetActPage.get_request()