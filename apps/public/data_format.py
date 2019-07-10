#coding:utf-8

def resData(code, msg, data):
    if not isinstance(data, dict):
        data = {}

    rdata = {
        "code": code,
        "msg": msg,
        "data": data
    }

    return rdata


