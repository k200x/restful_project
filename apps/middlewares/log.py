import time
import json
import logging
import logging.config

from flask import g,request
from apps.public.cheek_token import cheek



def before_request():
    setattr(request, 'start_time', time.time())
    request.token = request.values.to_dict().get("logintoken", "")
    #request.values = request.values.to_dict()
    request.req_values = request.values.to_dict()
    if request.token:
        request.uoid = cheek(request.token)
    else:
        request.uoid = " "



# 签名认证


def after_request(response):
    # 解决跨域
    response.headers['Access-Control-Allow-Origin'] = "*"  # 所有域名
    response.headers['Access-Control-Allow-Methods'] = "POST" # 指定方法
    response.headers['Access-Control-Allow-Headers'] = "x-requseted-with,content-type"
    response.headers["Content-type"] = "application/json"
    return response



def teardown_request(exc):
    print(request.values.to_dict())
    print(type(request.values.to_dict()))
    if "password" in request.req_values:
        print("1===")
        request.req_values["password"] = "*******"
        print(request.req_values)

    try:

        logInfo = {
            "method": request.method,
            "url": request.url,
            "requestTime": time.time() - getattr(request, 'start_time', 0),
            "uoid": request.uoid,
            "reqData": request.req_values,
            "resData": request.logInfo,
        }
        logInfo = json.dumps(logInfo)
        logger = logging.getLogger("logInfo")
        logger.info(logInfo)

    except Exception as e:
        logger = logging.getLogger("log_error")
        logger.warning(e)




