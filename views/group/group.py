from flask import Blueprint

from .group_good import GroupGood, GroupDetail, StartGroup
from .group_nav import GroupNav

group = Blueprint('group', __name__, url_prefix='/v4')


@group.route('/getGroupGood')
def get_group_good():
    return GroupGood.get_request()


@group.route('/getGroupNav')
def get_group_nav():
    return GroupNav.get_request()


@group.route('/group_detail')
def group_detail():
    return GroupDetail.get_request()