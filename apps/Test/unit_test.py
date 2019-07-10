#coding:utf-8


import json
import unittest
from apps import app

class RegisterTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_register(self):
        """测试用户名与密码为空的情况[当参数不全的话，返回errcode=-2]"""
        response = app.test_client().post('/register', data={"username": "aaaaa", "password": "12343", "phone_number": "18600766147", "role_type": "1"})
        json_data = response.data
        json_dict = json.loads(json_data)

        self.assertIn('errcode', json_dict, '数据格式返回错误')
        self.assertEqual(json_dict['errcode'], -2, '状态码返回错误')

        # TODO 测试用户名为空的情况

        # TODO 测试密码为空的情况

    def test_login(self):
        """测试用户名和密码错误的情况[当登录名和密码错误的时候，返回 errcode = -1]"""
        response = app.test_client().post('/login', data={})
        json_data = response.data
        json_dict = json.loads(json_data)
        self.assertIn('errcode', json_dict, '数据格式返回错误')
        self.assertEqual(json_dict['errcode'], -1, '状态码返回错误')

        # TODO 测试用户名错误的情况

        # TODO 测试密码错误的情况


class FeatureBuyAndGetTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_but_feature(self):
        pass

    def test_get_feature(self):
        pass

    def test_get_feature_count(self):
        pass

class FeatureRunTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_empty_username_password(self):
        pass

    def test_error_username_password(self):
        pass


if __name__ == '__main__':
    pass
