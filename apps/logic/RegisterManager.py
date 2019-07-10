#coding:utf-8

# for decorator
from apps.decorator.singleton import singleton
# for db engine
from apps.db_engine import mongo_obj, redis_obj
# for utilities
import hashlib

@singleton
class RegisterManager(object):
    def __init__(self):
        pass

    def register(self, user_id, password, role_type, phone_number=""):
        user_info = mongo_obj.conn.find_one({"user_id": user_id})

        if not user_info:
            data = {
                "user_id": user_id,
                "password": self.__encryption(password),  # encryption
                "role_type": role_type,
                "phone_number": phone_number
            }
            mongo_obj.conn.userData.user_info.insert_one(data)
            return True

        return False

    def login(self):
        pass

    def login_check(self, user_id, password):
        user_info = mongo_obj.conn.userData.user_info.find_one({'user_id': user_id})
        if not user_info:
            return None

        # 对比输入的密码和数据库的密码是否相同
        password_in_db = user_info.get("password", "")
        password_md5 = self.encryption(password)
        if password_md5 == password_in_db:
            return user_info

    def __encryption(pw):
        m = hashlib.md5()
        password = 'sI+#!-ml%se' % pw
        m.update(password.encode('utf-8'))
        pw_md5 = m.hexdigest().upper()
        return pw_md5



register_manager = RegisterManager()