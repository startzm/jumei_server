
from flask import Blueprint

from views.group.group_good import StartGroup
from .get_page import GetMine, GetLogin, ShowPhoto
from .regist import Regist
from .login import PhoneLogin, AccountLogin
from .send_message import SendMessage
from .verify_user import VerifyUser
from .history import GetHistory, GoodHistory
from .cart import AddCart, GetCart, RemoveCart, GetCartCount
from .recommend import PeopleBought, PersonalRecommend
from .order import CreateOrder, GetOrderInfo, GetOrder
from .payment import GetPaymethod, Payment
from .order_detail import OrderDetail, OrderReceived, OrderComment
from .comment import GoodComment, ShowCommentPhoto
from .information import GetInformation, GetInformationPage, GetInformationCount

user = Blueprint('user', __name__, url_prefix='/v5')


@user.route('/get_mine')
def get_mine():
    return GetMine.get_request()


@user.route('/get_login')
def get_login():
    return GetLogin.get_request()


@user.route('/regist', methods=['POST'])
def regist():
    return Regist.get_request()


@user.route('/login', methods=['POST'])
def login():
    return AccountLogin.get_request()


@user.route('/phone_login', methods=['POST'])
def phone_login():
    return PhoneLogin.get_request()


@user.route('/send_message')
def send_message():
    return SendMessage.get_request()


@user.route('/good_history')
def good_history():
    return GoodHistory.get_request()


@user.route('/verify_user')
def verify_user():
    return VerifyUser.get_request()


@user.route('/get_history')
def get_history():
    return GetHistory.get_request()


@user.route('/add_cart', methods=['POST'])
def add_cart():
    return AddCart.get_request()


@user.route('/remove_cart', methods=['POST'])
def remove_cart():
    return RemoveCart.get_request()


@user.route('/get_cart')
def get_cart():
    return GetCart.get_request()


@user.route('/get_cart_count')
def get_cart_count():
    return GetCartCount.get_request()


@user.route('/people_bought')
def people_bought():
    return PeopleBought.get_request()


@user.route('/personal_recommend')
def personal_recommend():
    return PersonalRecommend.get_request()


@user.route('/create_order', methods=['POST'])
def create_order():
    return CreateOrder.get_request()


@user.route('/get_order_info', methods=['POST'])
def get_order_info():
    return GetOrderInfo.get_request()


@user.route('/get_order')
def get_order():
    return GetOrder.get_request()


@user.route('/get_paymethod')
def get_paymethod():
    return GetPaymethod.get_request()


@user.route('/payment', methods=['POST'])
def payment():
    return Payment.get_request()


@user.route('/order_detail', methods=['GET'])
def order_detail():
    return OrderDetail.get_request()


@user.route('/order_received', methods=['GET'])
def order_received():
    return OrderReceived.get_request()


@user.route('/order_comment', methods=['GET'])
def order_comment():
    return OrderComment.get_request()


@user.route('/show/<string:filename>', methods=['GET'])
def show_img(filename):
    return ShowPhoto.get_request(filename)


@user.route('/start_group', methods=['POST'])
def start_group():
    return StartGroup.get_request()


@user.route('/submit_comment', methods=['POST'])
def submit_comment():
    return GoodComment.get_request()


@user.route('/show_comment/<string:filename>', methods=['GET'])
def show_comment(filename):
    return ShowCommentPhoto.get_request(filename)


@user.route('/get_information')
def get_information():
    return GetInformation.get_request()


@user.route('/get_information_page')
def get_information_page():
    return GetInformationPage.get_request()


@user.route('/get_chat_count')
def get_chat_count():
    return GetInformationCount.get_request()