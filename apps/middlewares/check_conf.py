from apps.db_engine import mongo_obj
from apps import config

def before_request():
    update_time = mongo_obj.conn.userCenterConfig.config.find_one({"table":"config"},{"lastActiontime":1})
    new_time = update_time.get('lastActiontime',0)
    load_ts = config.user.load_ts
    if new_time > load_ts:
        config.user.reload()
        config.user.update_ts(new_time)
