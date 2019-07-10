import time
from apps.db_engine import mongo_obj

class User(object):
    def __init__(self):
        self._load_ts = time.time()
        self._config = {}

    def init(self):
        self.reload()

    def reload(self):
        self._config = mongo_obj.conn.userCenterConfig.config.find_one({"table":"config"})
        return self._config

    def get(self,name,default=""):
        return self._config.get(name,default)

    @property
    def load_ts(self):
        return self._load_ts

    def update_ts(self,times):
        self._load_ts = times




user = User()

def init():
    user.init()




