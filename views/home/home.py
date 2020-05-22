from flask import Blueprint

from .home_nav import HomeNav
from .home_act import HomeAct
from .home_good import HomeGood

home = Blueprint('home', __name__, url_prefix='/home')


@home.route('/nav')
def get_home_nav():
    return HomeNav.get_request()


@home.route('/act')
def get_home_act():
    return HomeAct.get_request()


@home.route('/good')
def get_home_good():
    return HomeGood.get_request()