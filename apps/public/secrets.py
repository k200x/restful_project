import time
import hashlib
import logging

from constant import TOKEN_PREFIX
from apps.db_engine import redis_obj





_S_PRE = "sM!L2m@j7an9"

class Secrets(object):

    def __init__(self,token):
        self.token = token

    def get_secrets(self):
        '''
        :param token: logintoken
        :return: secrets
        '''

        try:
            result = redis_obj.get(TOKEN_PREFIX + self.token)
        except Exception as e:
            raise e

        secrets = result.get("secrets", "")

        return secrets

    def generate_secrets(self):
        # -s 签名
        t = str(time.time())
        secrets = hashlib.md5((_S_PRE + t).encode()).hexdigest()
        return secrets

    def update_secrets(self):

        try:
            result = redis_obj.get(TOKEN_PREFIX + self.token)
        except Exception as e:
            raise e

        s = self.generate_secrets()
        result["secrets"] = s

        try:
            secrets = redis_obj.update(TOKEN_PREFIX + self.token, result)
        except Exception as e:
            raise e
        if secrets:
            return result
        else:
            return {}







