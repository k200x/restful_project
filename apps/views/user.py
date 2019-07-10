# -*- coding: utf-8 -*-

# for framework
from flask import request, jsonify, Blueprint
# for db engine
# for system model
from apps.logic.RegisterManager import register_manager

# for utilities
import logging
from apps.public.data_format import resData

# for log
bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/register', methods=['POST'])
def register():

    log = logging.getLogger("log_error")

    if request.method == "POST":
        # 获取参数
        user_id = request.values.get('user_id')
        password = request.values.get('password')
        phone_number = request.values.get('phone_number')
        role_type = request.values.get('role_type')

        r_data = None
        if not user_id or not password or not role_type:
            r_data = resData(-1000, "lack of data", {})
        else:
            # 注册
            register_status = register_manager.register(user_id, password, role_type, phone_number)
            if register_status:
                r_data = resData(1000, "register success", {})
            else:
                r_data = resData(-2000, "user already exist", {})

        return jsonify(r_data)


@bp.route('/login', methods=['POST'])
def race_center_login():
    if request.method == "POST":
        user_id = request.values.get('user_id')
        password = request.values.get('password')
        role_type = request.values.get("role_type", "")

        # 获取数据库用户名
        user_check = False
        user_info = None
        # 判断用户是否存在，尝试3次
        for i in range(3):
            try:
                user_info = register_manager.login_check()
                if user_info:
                    user_check = True
                    break
            except Exception as e:
                print(str(e))  # or using trackback
                user_check = False

        res_data = None
        if user_check:
            res_data = resData(1000, "success", user_info.get("user_base_info"))
        else:
            res_data = resData(-1000, "failure", {})

        return jsonify(res_data)







