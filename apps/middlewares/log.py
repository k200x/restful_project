import time
import json
import logging
import logging.config

from flask import g,request

def before_request():
    pass

def after_request(response):
    # 解决跨域
    response.headers['Access-Control-Allow-Origin'] = "*"  # 所有域名
    response.headers['Access-Control-Allow-Methods'] = "POST"  # 指定方法
    response.headers['Access-Control-Allow-Headers'] = "x-requseted-with,content-type"
    response.headers["Content-type"] = "application/json"
    return response

def teardown_request(exc):
    pass




