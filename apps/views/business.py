#coding:utf-8

from flask import request, jsonify, Blueprint

# for utilities
from apps.public.data_format import resData

# for system model
from apps.logic.UserManager import user_manager
from apps.logic.FeatureManager import feature_manager

bb = Blueprint('business', __name__, url_prefix='/business')

@bb.route('buy_features', methods=['POST'])
def buy_features():

    user_id = request.values.get('user_id', "")
    feature_list = request.values.get('feature_list', "")

    if user_id and feature_list:
        user_manager.buy_features(user_id, feature_list)
        r_data = resData(1000, "success", {})
    else:
        r_data = resData(-1000, "failure", {})

    return jsonify(r_data)

@bb.route('get_features', methods=['POST'])
def get_features():
    '''获取单个用户的功能'''
    user_id = request.values.get('user_id', "")

    if user_id:
        # get features
        user_manager.get_features(user_id)
        r_data = resData(1000, "success", {})
    else:
        r_data = resData(-1000, "failure", {})

    return jsonify(r_data)

@bb.route('get_feature_user_count', methods=['POST'])
def get_feature_user_count():
    '''获取单个功能拥有的人数'''
    feature_id = request.values.get('feature_id', "")

    if feature_id:
        # get feature user count
        count = feature_manager.get_feature_user_count(feature_id)
        r_data = resData(1000, "success", {"count": count})
    else:
        r_data = resData(-1000, "failure", {})

    return jsonify(r_data)




