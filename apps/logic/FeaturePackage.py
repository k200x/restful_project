#coding:utf-8

class BaseFeature(object):
    def __init__(self, id):
        self.feature_id = id
        self.feature_package = None

class GeneralFeature(BaseFeature):
    def __init__(self):
        pass

class Feature_One(BaseFeature):
    def __init__(self):
        pass

class Feature_Two(BaseFeature):
    def __init__(self):
        pass





class Developers_Feature(Feature_One):
    '''开发商功能包'''
    def __init__(self):
        pass


class Designing_Institute_Feature(Feature_Two):
    '''设计院功能包'''
    def __init__(self):
        pass



class FeatureFactory(object):
    def __init__(self):
        pass



