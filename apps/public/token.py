import hashlib
import time
import json
import re

from apps.db_engine import redis_obj

TOKEN_S = 'sm%sile%f'

class Token(object):

    def __init__(self,uoid):

        # "project_m|role|59c331b3ba79991bf96f658c" 前缀+uoid
        self.role_prefix = "project_m|role|"
        # "project_m|token|130df2d3d021b728cb1225281fe3fa2d" 前缀+new_token
        self.token_prefix = "project_m|token|"
        # rid-->uoid
        self.rid = uoid
        # 缓存用于存储临时变量
        self.cache = ""
        self.oldToken = ""

    def bytes_to_dic(self,key):

        if isinstance(key, dict):
            return key
        if isinstance(key, bytes):
            result = str(key.decode("utf-8"))
            result = re.sub('\'', '\"', result)

        result = json.loads(result)

        return result


    def generate_token(self):
        '''
        生成token
        :return: 
        '''
        new_token = hashlib.md5((TOKEN_S % (self.rid, time.time())).encode()).hexdigest()
        return new_token


    def get_token_dic(self,token):
        try:
            Ddata = redis_obj.get(self.token_prefix + token)
        except Exception as e:
            raise e
        if Ddata:
            result = self.bytes_to_dic(Ddata)
        else:
            result = {}
        return result

    def get_role_dic(self,token):
        try:
            Ddata = redis_obj.get(self.role_prefix + self.rid )
        except Exception as e:
            raise e
        if Ddata:
            result = self.bytes_to_dic(Ddata)
        else:
            result = {}
        return result

    def get_db_token(self,token):
        Ddata = self.get_role_dic(token)
        dbtoken = Ddata.get("token", "")

        return dbtoken



    def get_token_loginMode(self, token):
        Ddata = self.get_token_dic(token)
        loginMode = Ddata.get("loginMode", "")
        third = Ddata.get("third", "")
        data = {
            "loginMode":loginMode,
            "third":third
        }
        return data



    # 更新角色的token记录
    def update_role_token(self):

        try:
            Ddata = redis_obj.get(self.role_prefix + self.rid)
        except Exception as e:
            raise e

        if Ddata:

            result_dic = self.bytes_to_dic(Ddata)
            self.oldToken = result_dic.get("token") # 记录老的token
            print("更新获取老token")
            print(self.oldToken)

            new_token = self.generate_token()
            result_dic["updated"] = time.time()
            result_dic["token"] = new_token
        try:
            result = redis_obj.update(self.role_prefix + self.rid, result_dic)
        except Exception as e:
            raise e
        if result:
            # 缓存最新token
            self.cache = new_token
            return new_token
        else:
            return ""




    def created_role_uoid(self):
        # 创建角色的token记录
        if self.cache:
            new_token = self.cache
        else:
            new_token = self.generate_token()
        value ={
                "created":time.time(),
                "updated": time.time(),
                "token": new_token
                }
        try:
            key = self.role_prefix + self.rid
            count = redis_obj.keys(key)
            if count:
                Ddata = redis_obj.get(key)
                Ddata_dic = self.bytes_to_dic(Ddata)
                self.oldToken = Ddata_dic.get("token")
                redis_obj.rem(key)
            result = redis_obj.add(key, value)
            redis_obj.expire(key,86400*7)
        except Exception as e:
            raise e
        if result:
            self.cache = new_token

            return value
        else:
            return {}




    def created_token_token(self,loginMode="", third="",mode=""):


        if self.cache:
            new_token = self.cache
        else:
            self.cache = self.generate_token()
            new_token = self.generate_token()

        # {'rid': self.rid, 'secrets': self.new_secrets, "loginMode": loginMode, "third": third}
        value = {
            "rid":self.rid,
            "loginMode":loginMode,
            "third":third,
            "mode":mode
        }

        try:
            result = redis_obj.add(self.token_prefix + new_token, value)
            redis_obj.expire(self.token_prefix + new_token, 86400 * 7)
            # 删除老的token
            print("token_old")
            print(self.oldToken)
            if self.oldToken:
                key = self.token_prefix + self.oldToken
                redis_obj.rem(key)
        except Exception as e:
            raise e

        if result:
            self.cache = new_token
            return value
        else:
            return {}

def bytes_to_dic(key):

    if isinstance(key, dict):
        return key
    if isinstance(key, bytes):
        result = str(key.decode("utf-8"))
        result = re.sub('\'', '\"', result)

    result = json.loads(result)

    return result


def get_usercenter_token(token):
    token_prefix = "project_m|token|"
    try:
        Ddata = redis_obj.get(token_prefix + token)
    except Exception as e:
        raise e
    if Ddata:
        result = bytes_to_dic(Ddata)
    else:
        result = {}
    return result

