#coding:utf-8

from apps.db_engine import mongo_obj, redis_obj

class FeaturesManager(object):

    def __init__(self, name_length):
        self.name = self.__init_name(name_length)
        self.features_list = []

    def __init_name(self, name_length):
        '''初始化功能包名字'''
        name_str = ""

        lower_case_char = [chr(i) for i in range(97, 97 + 26)]
        upper_case_char = [chr(i) for i in range(65, 65 + 26)]

        total_char = lower_case_char + upper_case_char

        for i in range(len(name_length)):
            index = random.randint(0, len(total_char) - 1)
            name_str += chr(index)

        return name_str

    def buy_features(self):
        '''购买功能包'''
        pass



if __name__ == "__main__":
    import random
    print(random.randint(10))






