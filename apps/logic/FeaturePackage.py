#coding:utf-8

import random

class BaseFeature(object):
    def __init__(self, id):
        self.feature_id = id
        self.feature_package = None

    def run(self):
        pass

class GeneralFeature(BaseFeature):
    def __init__(self):
        pass

    def run(self):
        pass

class Feature_One(BaseFeature):
    def __init__(self):
        pass

    def run(self):
        pass

class Feature_Two(BaseFeature):
    def __init__(self):
        pass

    def run(self):
        pass

class Developers_Feature(Feature_One):
    '''开发商功能包'''
    def __init__(self):
        pass

    def run(self):
        pass


class Designing_Institute_Feature(Feature_Two):
    '''设计院功能包'''
    def __init__(self):
        pass

    def run(self):
        pass

class FeatureFactory(object):

    def __init__(self):
        self.features = {}

    def __create_name(self, name_str_length):
        '''初始化功能包名字'''
        name_str = ""

        lower_case_char = [chr(i) for i in range(97, 97 + 26)]
        upper_case_char = [chr(i) for i in range(65, 65 + 26)]

        total_char = lower_case_char + upper_case_char

        for i in range(len(name_str_length)):
            index = random.randint(0, len(total_char) - 1)
            name_str += chr(index)

        return name_str

    def init_features(self):
        # 可以根据需求定制，或者用策略模式什么的，根据需求预设功能
        for i in range(100):
            self.features[self.__create_name(10)] = Developers_Feature()

        return self.features




