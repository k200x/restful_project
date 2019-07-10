#coding:utf-8

# for decorator
from apps.decorator.singleton import singleton

# for system model
from apps.logic.FeatureManager import feature_manager

# for db engine
from apps.db_engine import mongo_obj, redis_obj

@singleton
class UserManager(object):
    def __init__(self):
        pass

    def buy_features(self, user_id, feature_id):
        # 一个功能一个table，用于记录玩家信息
        user_list = mongo_obj.conn.featureData.player_info.find_one({"feature_id": feature_id})
        user_list.append(user_id)
        mongo_obj.conn.featureData.player_info.update({"feature_id": feature_id}, {"$set": {"user_list": user_list}})

        # 玩家也记录一个名称映射，从而知道这个玩家有哪些功能
        # 从而避免互相查找的大量遍历
        feature_list = mongo_obj.conn.featureData.player_info.find_one({"user_id": user_id})
        feature_list.append(feature_id)
        mongo_obj.conn.playerData.feature_info.insert_one({"user_id": user_id}, {"$set": {"feature_list": feature_list}})

    def get_features(self, user_id):
        feature_info = mongo_obj.conn.playerData.feature_info.find_one({"user_id": user_id})
        if feature_info:
            feature_list = feature_info.get("feature_list")
            feature_manager.run_features(feature_list)


user_manager = UserManager()






