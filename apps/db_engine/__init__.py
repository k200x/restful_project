import redis
import re
import json
import pymongo

from settings.local import redis_db, mongo_db

class MongoDB(object):
    def __init__(self, table):
        self.table = table

    def insert(self, data):

        # 重连数据库抛出异常
        for i in range(NUMBERS):
            try:
                result = self.table.insert_one(data)
                controller = False
                break
            except Exception as f:
                e = f
                controller = True
        if controller:
            raise e

        return result

    def get(self, conditions, data=None):
        if data:
            mdata = {data: 1}
        else:
            mdata = None

        # 重连数据库抛出异常
        for i in range(NUMBERS):
            try:
                result = self.table.find_one(conditions, mdata)
                controller = False
                break
            except Exception as f:
                e = f
                controller = True
        if controller:
            raise e

        if not result:
            result = {}
        return result

    def update(self, conditions, data, multi=False):

        # conn.player.player.update({"userId": g.uoid}, {"$set": {"roledata.nickSet": 1, "nick": name}})
        udata = {"$set": data}
        for i in range(NUMBERS):
            try:
                result = self.table.update(conditions, udata, multi=multi)
                controller = False
                break
            except Exception as f:
                e = f
                controller = True
        if controller:
            raise e

        # 返回 {'n': 1, 'nModified': 0, 'ok': 1.0, 'updatedExisting': True}
        return result

    def remove(self, conditions, multi=False):

        if not conditions:
            if multi:
                conditions = {}
            else:
                conditions = ""

        for i in range(NUMBERS):
            try:
                result = self.table.remove(conditions)
                controller = False
                break
            except Exception as f:
                e = f
                controller = True
        if controller:
            raise e

        return result

    def count(self, conditions):

        for i in range(NUMBERS):
            try:
                result = self.table.count(conditions)
                controller = False
                break
            except Exception as f:
                e = f
                controller = True
        if controller:
            raise e

        return result

class RedisDB(object):

    def __init__(self, **kwargs):

        self.conn = redis.StrictRedis(**kwargs)

    def convert(self,data):
        if isinstance(data, bytes):
            return data.decode('utf-8')
        if isinstance(data, dict):
            return dict(map(convert, data.items()))
        if isinstance(data, tuple):
            return map(convert, data)
        return data

    def json_format(self,data):
        result = re.sub('\'', '\"', data)
        return result

    def conn(self):
        return self.conn

    def keys(self, key):
        # 重连数据库抛出异常
        for i in range(NUMBERS):
            try:
                Ddata = self.conn.keys(key)
                controller = False
                break
            except Exception as f:
                e = f
                controller = True
        if controller:
            raise e
        Ddata_list = self.convert(Ddata)
        return Ddata_list

    def expire(self,key, time):
        self.conn.expire(key, time)


    def add(self, key, value):
        result = self.conn.set(key, value)
        return result

    def get(self, key):
        '''
        
        :param key:查询的key
        :return: 字典,查询不到报错
        '''
        # 重连数据库抛出异常
        for i in range(NUMBERS):
            try:
                Ddata = self.conn.get(key)
                controller = False
                break
            except Exception as f:
                e = f
                controller = True
        if controller:
            raise e
        # 转换为字典
        Ddata_str = self.convert(Ddata)
        Ddata_json = self.json_format(Ddata_str)
        result = json.loads(Ddata_json)
        return result

    # 修改
    def update(self, key, value):
        # 重连数据库抛出异常
        for i in range(NUMBERS):
            try:
                result = self.conn.get(key)
                controller = False
                break
            except Exception as f:
                e = f
                controller = True
        if controller:
            raise e


        if result:

            # 重连数据库抛出异常
            for i in range(NUMBERS):
                try:
                    result2 = self.conn.set(key, value)
                    controller = False
                    break
                except Exception as f:
                    e = f
                    controller = True
            if controller:
                raise e

            return result2
        else:
            print("key " + key + "is not found")

    def rem(self,key):
        # 重连数据库抛出异常
        for i in range(NUMBERS):
            try:
                result = self.conn.delete(key)
                controller = False
                break
            except Exception as f:
                e = f
                controller = True
        if controller:
            raise e

        if result != 0:
            return result

    # 以下为哈希类型
    def hgetall(self, key):

        # 重连数据库抛出异常
        for i in range(NUMBERS):
            try:
                Ddata = self.conn.hgetall(key)
                controller = False
                break
            except Exception as f:
                e = f
                controller = True
        if controller:
            raise e
        result = self.convert(Ddata)
        return result

    def hdel(self,name,*key):
        # 重连数据库抛出异常
        for i in range(NUMBERS):
            try:
                result = self.conn.hdel(name,*key)
                controller = False
                break
            except Exception as f:
                e = f
                controller = True
        if controller:
            raise e
        return result



    def hget(self,name,key):
        # 重连数据库抛出异常
        for i in range(NUMBERS):
            try:
                Ddata = self.conn.hget(name,key)
                controller = False
                break
            except Exception as f:
                e = f
                controller = True
        if controller:
            raise e
        result = self.convert(Ddata)
        return result


    def hset(self,name,key,value):
        # 重连数据库抛出异常
        for i in range(NUMBERS):
            try:
                result = self.conn.hset(name,key, value)
                controller = False
                break
            except Exception as f:
                e = f
                controller = True
        if controller:
            raise e

        return result



    def hmset(self,key,map):
        # 重连数据库抛出异常
        for i in range(NUMBERS):
            try:
                result = self.conn.hmset(key, map)
                controller = False
                break
            except Exception as f:
                e = f
                controller = True
        if controller:
            raise e

        return result

    def hlen(self,key):
        # 重连数据库抛出异常
        for i in range(NUMBERS):
            try:
                result = self.conn.hlen(key)
                controller = False
                break
            except Exception as f:
                e = f
                controller = True
        if controller:
            raise e

        return result



    # 以下为列表类型
    def lpop(self,key):
        # 重连数据库抛出异常
        for i in range(NUMBERS):
            try:
                Ddata = self.conn.lpop(key)
                controller = False
                break
            except Exception as f:
                e = f
                controller = True
        if controller:
            raise e

        result = self.convert(Ddata)
        return result


    def rpush(self,key,*values):
        # 重连数据库抛出异常
        for i in range(NUMBERS):
            try:
                result = self.conn.rpush(key,*values)
                controller = False
                break
            except Exception as f:
                e = f
                controller = True
        if controller:
            raise e
        return result


redis_obj = RedisDB(**redis_db)
mongo_obj = MongoDB(**mongo_db)

