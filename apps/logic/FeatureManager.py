#coding:utf-8

# for database
from apps.db_engine import mongo_obj, redis_obj
# for decorator
from apps.decorator.singleton import singleton
# for system model
from apps.logic.FeaturePackage import FeatureFactory

@singleton
class FeaturesManager(object):
    def __init__(self, name_length):
        self.factory = FeatureFactory()
        # 预设置功能
        self.features = self.factory.init_features()

    def buy_features(self):
        '''购买功能包'''
        pass

    def run_features(self, feature_list):
        '''获取功能'''
        for feature_name in feature_list:
            self.features[feature_name].run()

    def get_feature_user_count(self, feature_id):
        user_list = mongo_obj.conn.featureData.feature_info.find_one({"feature_id": feature_id})
        return len(user_list)


feature_manager = FeaturesManager(100)

if __name__ == "__main__":
    import random
    print(random.randint(10))






