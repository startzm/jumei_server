from flask import Blueprint

from .category_list import GetCategoryList
from .sub_category import GetSubCategory

category = Blueprint('category', __name__, url_prefix='/v2')


@category.route('/get_category')
def get_category():
    return GetCategoryList.get_request()


@category.route('/get_sub')
def get_sub():
    return GetSubCategory.get_request()
