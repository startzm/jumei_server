from flask import Blueprint, render_template
from .login import AdminLogin
from .product import GetProduct, AddProduct, ChangeProduct
from .category import GetCategory
from .member import GetMember, ChangeMember
from .act import GetAct
from .user import GetAdmin
from .order import GetOrder, ChangeOrder

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/login')
def login():
    return AdminLogin.get_request()


@admin.route('/get_product')
def get_product():
    return GetProduct.get_request()


@admin.route('/add_product')
def add_product():
    return AddProduct.get_request()


@admin.route('/change_product')
def change_product():
    return ChangeProduct.get_request()


@admin.route('/get_category')
def get_category():
    return GetCategory.get_request()


@admin.route('/get_member')
def get_member():
    return GetMember.get_request()


@admin.route('/change_member')
def change_member():
    return ChangeMember.get_request()


@admin.route('/get_act')
def get_act():
    return GetAct.get_request()


@admin.route('/get_admin')
def get_admin():
    return GetAdmin.get_request()


@admin.route('/get_order')
def get_order():
    return GetOrder.get_request()


@admin.route('/change_order')
def change_order():
    return ChangeOrder.get_request()