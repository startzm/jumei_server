from flask import Blueprint

from .daily_lottery import GetLottery, JoinLottery
from .signin import Signin
from .coupon import GetCoupon, GetOrderCoupon
from .turntable import GetTurntable
from .address import AddAddress, GetAddress, RemoveAddress, ChangeAddress, GetDefaultAddress
from .integral import GetIntegral, GetIntegralRule, GetOrderIntegral
from .collect import GoodCollect, StoreCollect, RemoveGoodCollect, RemoveStoreCollect,\
    GetGoodStatus, GetStoreStatus, GetCollect
from .settings import GetRules, ChangePwd, UploadHeader, GetUserInfo, ChangeInfo, MessageSettings, ChangeMessageSettings
from .often_buy import OftenBuy
from .question import GetQuestionList, GetQuestionAnswer, GetQuestionPage
from .banding import GetBanding
from .wish import RemoveWish, GoodWish, GetWish

other = Blueprint('other', __name__, url_prefix='/v5')


@other.route('/get_lottery')
def get_lottery():
    return GetLottery.get_request()


@other.route('/signin')
def signin():
    return Signin.get_request()


@other.route('/get_coupon')
def get_coupon():
    return GetCoupon.get_request()


@other.route('/get_turntable')
def get_turntable():
    return GetTurntable.get_request()


@other.route('/join_lottery', methods=['POST'])
def join_lottery():
    return JoinLottery.get_request()


@other.route('/get_integral')
def get_integral():
    return GetIntegral.get_request()


@other.route('/add_address', methods=['POST'])
def add_address():
    return AddAddress.get_request()


@other.route('/get_address')
def get_address():
    return GetAddress.get_request()


@other.route('/get_default_address')
def get_default():
    return GetDefaultAddress.get_request()


@other.route('/remove_address', methods=['POST'])
def remove_address():
    return RemoveAddress.get_request()


@other.route('/change_address', methods=['POST'])
def change_address():
    return ChangeAddress.get_request()


@other.route('/good_collect')
def good_collect():
    return GoodCollect.get_request()


@other.route('/store_collect')
def store_collect():
    return StoreCollect.get_request()


@other.route('/remove_good_collect')
def remove_good_collect():
    return RemoveGoodCollect.get_request()


@other.route('/remove_store_collect')
def remove_store_collect():
    return RemoveStoreCollect.get_request()


@other.route('/get_good_status')
def get_good_status():
    return GetGoodStatus.get_request()


@other.route('/get_store_status')
def get_store_status():
    return GetStoreStatus.get_request()


@other.route('/get_collect')
def get_collect():
    return GetCollect.get_request()


@other.route('/get_rules')
def get_rules():
    return GetRules.get_request()


@other.route('/set_password', methods=['POST'])
def set_password():
    return ChangePwd.get_request()


@other.route('/upload_header', methods=['POST'])
def upload_header():
    return UploadHeader.get_request()


@other.route('/get_user_info')
def get_user_info():
    return GetUserInfo.get_request()


@other.route('/change_info', methods=['POST'])
def change_info():
    return ChangeInfo.get_request()


@other.route('/often_buy')
def often_buy():
    return OftenBuy.get_request()


@other.route('/get_integral_rule')
def get_integral_rule():
    return GetIntegralRule.get_request()


@other.route('/get_order_coupon')
def get_order_coupon():
    return GetOrderCoupon.get_request()


@other.route('/get_question_page')
def get_question_page():
    return GetQuestionPage.get_request()


@other.route('/get_question_list')
def get_question_list():
    return GetQuestionList.get_request()


@other.route('/get_question_answer')
def get_question_answer():
    return GetQuestionAnswer.get_request()


@other.route('/get_banding')
def get_banding():
    return GetBanding.get_request()


@other.route('/get_wish')
def get_wish():
    return GetWish.get_request()


@other.route('/remove_wish')
def remove_wish():
    return RemoveWish.get_request()


@other.route('/good_wish')
def good_wish():
    return GoodWish.get_request()


@other.route('/get_order_integral')
def get_order_integral():
    return GetOrderIntegral.get_request()


@other.route('/get_message_settings')
def get_message_settings():
    return MessageSettings.get_request()


@other.route('/set_message_settings', methods=['POST'])
def set_message_settings():
    return ChangeMessageSettings.get_request()