# -*- coding: utf-8 -*-

import re
import time
import logging

from flask import request, jsonify, Blueprint, g

from apps.public.token import Token, get_usercenter_token
from apps.db_engine import mongo_obj
from constant import NUMBERS
from apps.public.encryption import encryption
from apps.public.word_filter import word_filter
from screen import l1

from apps.logic.PlayerInfo import player_info

import ltlog

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



        pc = request.values.get("pc",-100)
        mode = request.values.get("mode","") # 账号注册方式（ios，Android）
        # 判断用户格式
        res = re.compile(r'\w')
        res_z = re.compile(r'.*?[\u4E00-\u9FA5]')
        res_list = res.findall(username)
        if len(username) != len(res_list) or len(username) <= 6 or len(username) >= 20:
            data = {
                "code": -1004,
                "msg": "username invalid",
                'data': ""

            }
            request.logInfo = data
            return jsonify(data)

        if res_z.findall(username):
            data = {
                "code": -1004,
                "msg": "username invalid",
                'data': ""

            }
            request.logInfo = data
            return jsonify(data)

        # 屏蔽关键字
        # print("username")
        # print(username)
        # result = word_filter(l1, username)
        # print(result)
        # if result:
        #     data = {
        #         "code": -1008,
        #         "msg": "Lack of parameter",
        #         "data": ""
        #     }
        #
        #     return jsonify(data)

        # 判断密码格式
        if not (len(password) >= 6 and len(password) <= 16):
            data = {
                "code": -1007,
                "msg": "password invalid",
                "data": ""

            }
            request.logInfo = data
            return jsonify(data)

        # 判断用户是否存在
        conn = mongo_obj.conn
        # count = conn.usercenter.user.find_one({'username': username})

        for i in range(NUMBERS):
            try:
                count = conn.usercenter.user.find_one({'username': username})
                print(count)
                controller = False
                break
            except Exception as e:
                log.warning(e)
                controller = True
        if controller:
            data = {
                "code": -1005,
                "msg": "Database query failed",
                "data": ""
            }
            request.logInfo = data
            return jsonify(data)

        if count:
            data = {
                "code": -1006,
                "msg": "already registered",
                "data": ""

            }
            request.logInfo = data
            return jsonify(data)

        pw_md5 = encryption(password)
        createtime = time.time()

        # 获取用户ip
        register_ip = request.remote_addr

        data = {
            "username": username,
            "password": pw_md5,
            "userInfo": {"createtime": createtime, "register_ip": register_ip, "telephone": "", "email": "","mode":str(mode)}
        }
        #conn.usercenter.user.insert_one(data)

        for i in range(NUMBERS):
            try:
                conn.usercenter.user.insert_one(data)
                controller = False
                break
            except Exception as e:
                log.warning(e)
                controller = True

        if controller:
            data = {
                "code": -1005,
                "msg": "Database query failed",
                "data": ""
            }
            request.logInfo = data
            return jsonify(data)
        rep = {
            "code": 1000,
            "msg": "success",
            "data": {
                "mode": mode
            }
        }

        # 记录是否是pc注册用户
        if rep["code"] == 1000 and pc != -100:
            data["pc"] = int(pc)
            conn.usercenter.pcUser.insert_one(data)

        request.logInfo = rep
        return jsonify(rep)

@bp.route('/login', methods=['POST'])
def login():

    print(" ------ in login ------ ")

    if request.method == "POST":
        username = request.values.get('username')
        password = request.values.get('password')
        mode = request.values.get("mode", "")
        log = logging.getLogger("log_error")

        ltlog.info("^" * 80)

        # 获取数据库用户名
        conn = mongo_obj.conn

        for i in range(NUMBERS):
            try:
                db_username = conn.usercenter.user.find_one({'username': username})
                controller = False
                break
            except Exception as e:
                log.warning(e)
                controller = True
        if controller:
            data = {
                "code": -1005,
                "msg": "Database query failed",
                "data": ""
            }
            request.logInfo = data
            return jsonify(data)



        if not db_username:
            data = {
                "code": -1003,
                "msg": 'user not found',
                "data": ""
            }
            request.logInfo = data
            return jsonify(data)


        # 获取数据库中密码
        #db_password = db_username.get("password")


        for i in range(NUMBERS):
            try:
                db_password = db_username.get("password")
                controller = False
                break
            except Exception as e:
                log.warning(e)
                controller = True
        if controller:
            data = {
                "code": -1005,
                "msg": "Database query failed",
                "data": ""
            }
            request.logInfo = data
            return jsonify(data)


        pw_md5 = encryption(password)

        ltlog.info("username --- ", username)
        ltlog.info("password --- ", password)

        if db_password != pw_md5:
            data = {
                "code": -1002,
                "msg": 'password error',
                "data": ""
            }
            request.logInfo = data
            return jsonify(data)

        # 登陆验证
        dbMode = db_username["userInfo"]["mode"]
        # 过滤之前注册的账号
        if dbMode == "":
            conn.usercenter.user.update({'username': username}, {"$set": {"userInfo.mode": str(mode)}})
            dbMode = str(mode)

        if str(mode) != "2":  # 2为web登陆，不做验证
            if dbMode != str(mode):
                data = {
                    "code": -1002,
                    "msg": 'password error',
                    "data": ""
                }
                request.logInfo = data
                return jsonify(data)

        objectId_obj = conn.usercenter.user.find_one({'username': username})
        objectId = str(objectId_obj["_id"])

        # 生成token和secrets
        token_obj = Token(objectId)

        token_dic = token_obj.created_role_uoid()
        token = token_dic.get("token")
        token_obj.created_token_token(mode=mode)

        data = {
            "code": 1000,
            "msg": "success",
            "data": {
                "token": token,
                "mode": mode
            }
        }

        print(data)
        request.logInfo = data
        return jsonify(data)

@bp.route('/race_center_login', methods=['POST'])
def race_center_login():
    if request.method == "POST":
        username = request.values.get('username')
        password = request.values.get('password')
        mode = request.values.get("mode", "")

        # 获取数据库用户名
        conn = mongo_obj.conn
        res = mongo_obj.conn.usercenter.user.find_one({'username': username})
        if not res:
            data = {
                "code": -1000,
                "msg": 'user not exist',
                "data": {}
            }
            return jsonify(data)
        else:
            res_password = res["password"]

        pw_md5 = encryption(password)

        uoid = str(res["_id"])

        d = {
            "uoid": uoid
        }

        if res_password == pw_md5:
            data = {
                "code": 1000,
                "msg": 'password pass',
                "data": d
            }
        else:
            data = {
                "code": -1000,
                "msg": 'password error',
                "data": d
            }

        request.logInfo = data
        return jsonify(data)

@bp.route('/set_callboard_info', methods=['POST'])
def set_callboard_info():
    if request.method == "POST":
        # 获取数据库用户名
        conn = mongo_obj.conn

        d_info = {
            "updateList": [
                {
                    "update_time": "2019-02-20",
                    "update_content": [
                        "【赛事牌谱】和【选手统计】中的对局列表改为翻页模式1",
                        "【对局管理】增加对进行中的对局暂停管理，点击某场对局，可以手动暂停/继续该对局（单次暂停最多1个小时"
                    ]
                },
                {
                    "update_time": "2019-02-20",
                    "update_content": [
                        "【赛事牌谱】和【选手统计】中的对局列表改为翻页模式2",
                        "【对局管理】增加对进行中的对局暂停管理，点击某场对局，可以手动暂停/继续该对局（单次暂停最多1个小时"
                    ]
                },
                {
                    "update_time": "2019-02-20",
                    "update_content": [
                        "【赛事牌谱】和【选手统计】中的对局列表改为翻页模式3",
                        "【对局管理】增加对进行中的对局暂停管理，点击某场对局，可以手动暂停/继续该对局（单次暂停最多1个小时"
                    ]
                }
            ]
        }

        res = conn.race_center.callboard.insert(d_info)

        if not res:
            data = {"code": -1000, "msg": 'no data', "data": {}}
        else:
            data = {"code": 1000, "msg": 'success', "data": {}}

        request.logInfo = data
        return jsonify(data)

@bp.route('/create_race_admin', methods=['POST'])
def create_race_admin():
    if request.method == "POST":
        res = mongo_obj.conn.race_center.admin.find_one()
        if not res:
            mongo_obj.conn.race_center.admin.insert_one({})

        data = {"code": 1000, "msg": 'success', "data": {}}

        request.logInfo = data
        return jsonify(data)

@bp.route('/add_race_info', methods=['POST'])
def add_race_info():
    if request.method == "POST":
        res = mongo_obj.conn.race_center.race_info.find_one()
        if not res:
            d = {

                "race_info_list": [
                    {
                        "name": "aaaa",
                        "start_time": "2019-03-05 11:04:36",
                        "end_time": "2019-03-05 11:04:36",
                        "competitionId": "1000000"
                    },
                    {
                        "name": "aaaa",
                        "start_time": "2019-03-05 11:04:36",
                        "end_time": "2019-03-05 11:04:36",
                        "competitionId": "1000001"
                    },
                    {
                        "name": "aaaa",
                        "start_time": "2019-03-05 11:04:36",
                        "end_time": "2019-03-05 11:04:36",
                        "competitionId": "1000002"
                    },
                    {
                        "name": "aaaa",
                        "start_time": "2019-03-05 11:04:36",
                        "end_time": "2019-03-05 11:04:36",
                        "competitionId": "1000003"
                    },
                    {
                        "name": "aaaa",
                        "start_time": "2019-03-05 11:04:36",
                        "end_time": "2019-03-05 11:04:36",
                        "competitionId": "1000004"
                    }
                ]
            }

            mongo_obj.conn.race_center.race_info.insert(d)

        data = {"code": 1000, "msg": 'success', "data": {}}

        request.logInfo = data
        return jsonify(data)

@bp.route('/getPlayerInfoByUoid', methods=['POST'])
def getUoidInfo():
    if request.method == "POST":
        uoid = request.values.get("uoid", "")

        if not uoid:
            data = {"code": -1000, "msg": 'need uoid', "data": {}}
            return jsonify(data)

        res = player_info.getPlayerInfoByUoid()
        ltlog.info("^" * 100)
        ltlog.info("^" * 100)
        ltlog.info("^" * 100)
        ltlog.info(res)

        if not res:
            data = {"code": -1000, "msg": 'no data', "data": {}}
        else:
            data = {"code": 1000, "msg": 'success', "data": {}}

        request.logInfo = data
        return jsonify(data)

@bp.route('/callboard_info', methods=['GET'])
def callboard_info():
    if request.method == "GET":
        # 获取数据库用户名
        conn = mongo_obj.conn
        res = conn.race_center.callboard.find_one()

        d = {
            "info": [
                {
                    "date": "2019-3-23 10:10:10",
                    "update_content": [
                        "啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊"
                        "测试测试测试测试测试测试测试测试测试测试测试"
                    ]
                },
                {
                    "date": "2019-3-24 10:10:10",
                    "update_content": [
                        "啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊"
                        "测试测试测试测试测试测试测试测试测试测试测试"
                    ]
                },
                {
                    "date": "2019-3-25 10:10:10",
                    "update_content": [
                        "啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊"
                        "测试测试测试测试测试测试测试测试测试测试测试"
                    ]
                },
                {
                    "date": "2019-3-26 10:10:10",
                    "update_content": [
                        "啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊"
                        "测试测试测试测试测试测试测试测试测试测试测试"
                    ]
                }
            ]
        }

        if not res:
            data = {"code": -1000, "msg": 'no data', "data": {}}
        else:
            data = {"code": 1000, "msg": 'success', "data": d}

        request.logInfo = data
        return jsonify(data)


@bp.route('/get_token', methods=['POST'])
def get_token():
    token = request.values.get('token', "")
    data = get_usercenter_token(token)

    request.logInfo = data
    return jsonify(data)






