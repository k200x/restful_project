from apps.db_engine import mongo_obj, redis_obj

class PlayerInfo(object):

    def __init__(self):
        self.conn = mongo_obj.conn
        self.player_db = self.conn.player.player

    def getPlayerInfoByUoid(self, uoid):
        res = self.player_db.find_one({"uoid": uoid})
        return res

player_info = PlayerInfo()






