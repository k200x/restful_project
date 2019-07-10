import redis
import json
import re
import logging


from flask import g,jsonify
from constant import TOKEN_PREFIX,ROLE_PREFIX,NUMBERS
from apps.db_engine import redis_db


# 查询redis数据库
def cheek(token):

    '''
    
    :param token: 
    :return:rid,如果返回{},token过期 
    '''

    conn = redis.StrictRedis(**redis_db)
    token = TOKEN_PREFIX + token
    log = logging.getLogger("log_error")
    for i in range(NUMBERS):
        try:
            result = conn.get(token)
            controller = False
            break
        except Exception as f:
            controller = True
            result = None
            log.warning(f)
    print("--rid--")
    print(result)
    print("------")
    if controller:
        data = {
            "code": -1005,
            "msg": "Database query failed",
            "data": None
        }
        return jsonify(data)

    if not result:
        return {}

    result = str(result.decode("utf-8"))
    result = re.sub('\'', '\"', result)
    result = json.loads(result)
    rid = result.get("rid")
    return rid

def cheek_rid(rid):
    conn = redis.StrictRedis(**redis_db)
    role = ROLE_PREFIX + rid
    result = conn.get(role)
    if not result:
        return {}