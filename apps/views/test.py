# -*- coding: utf-8 -*-
'''
Created on 2019年3月28日

@author: 007
'''
from flask import request, jsonify, Blueprint
from apps.db_engine import redis_obj


bp = Blueprint('test', __name__, url_prefix='/test')

@bp.route("/tsname",methods=['GET'])
def set_Namtest_R():
    rname = request.values.get("rname","默认值")
    data={"rname":"Que_Ji_"+rname}
    return jsonify(data)


@bp.route("/setr",methods=['GET'])
def setRedis():
    rst=redis_obj.add("default", 101)
    if rst:
        data={"msg":"","state":0,"data":"default"}
        return jsonify(data)