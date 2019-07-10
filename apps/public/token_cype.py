import hashlib
import time
import redis
import json

from constant import TOKEN_PREFIX,ROLE_PREFIX
from apps.db_engine import redis_db,redis_obj

#
#
# class Token1(object):
#     def generate_token(self, rid):
#         self.token = hashlib.md5(('sm%sile%f' % (rid, time.time())).encode()).hexdigest()
#         return self.token
#
#     def generate_secrets(self, rid):
#         self.secrets = hashlib.md5(('sm%sile%f' % (rid, time.time())).encode()).hexdigest()
#         return self.secrets


class Token(object):

    def __init__(self,rid="",role_prefix=None,token_prefix=None):
        self.role_prefix = ROLE_PREFIX
        self.token_prefix = TOKEN_PREFIX
        self.rid = rid
        self.new_token = self.generate_token()
        self.secrets = self.generate_secrets()



    def redis_Byte_filter(self,key):
        import re
        result = str(key.decode("utf-8"))
        result = re.sub('\'', '\"', result)
        result = json.loads(result)
        return result


    def generate_token(self):
        self.token = hashlib.md5(('sm%sile%f' % (self.rid, time.time())).encode()).hexdigest()
        return self.token

    def generate_secrets(self):
        # -s 签名
        a = str(time.time())
        self.secrets = hashlib.md5(("sM!L2m@j7an9"+a).encode()).hexdigest()
        return self.secrets



    def token_key_value(self,token):
        '''
        
        :param token: 
        :return: 返回一个包含objectID，和secrets的字典
        '''

        self.token_value = redis_obj.get(self.token_prefix + token)

        if self.token_value:
            result = self.redis_Byte_filter(self.token_value)
        else:
            result = {}
        print(result)
        return result

    def role_key_token(self):
        print("role_key_value")
        self.role_value = redis_obj.get(self.role_prefix + self.rid)
        if self.role_value:
            result = self.redis_Byte_filter(self.role_value)
        else:
            result = {}
        return result


    def update_role_token(self,rid=""):

        '''
        "project_m|role|599e28e07441574e8eda2dcf"
        value = {
        "created": "1503537511.8793302",
        "updated": time.time(),
        "token": new_token
    }
        '''
        if rid:
            self.rid = rid

        result = redis_obj.get(self.role_prefix + self.rid)


        if result:
            import re

            result = str(result.decode("utf-8"))
            result = re.sub('\'', '\"', result)
            result = json.loads(result)
            self.new_token = self.generate_token()

            result["updated"] = time.time()

            result["token"] = self.new_token

            redis_obj.mod(self.role_prefix + self.rid, result)
        else:

            self.value = {"created": time.time(), "updated": time.time(), "token": self.new_token}
            redis_obj.add(self.role_prefix + self.rid,  self.value)

        return self.new_token

    def update_token_secrets(self):
        '''
          "rid": objectId,
        "secrets": new_secrets
        '''
        # get project_m|token|4354403aaab501520d565da70db81c09
        # "{'rid': '599e28e07441574e8eda2dcf', 'secrets': '0d74ec26f09daeac64f7b9de3511cbfe'}"


        self.new_secrets = self.generate_secrets()
        self.rid_secrets = {'rid': self.rid, 'secrets': self.new_secrets}
        redis_obj.add(self.token_prefix + self.new_token, self.rid_secrets)
        return self.new_secrets

    def add_role_token(self):
        pass

    def add_token_secrets(self):
        pass


    # 获取secrets
    def get_secrets(self,token):
        result = self.token_key_value(token)
        print(result)
    # --------




