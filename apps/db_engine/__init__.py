import redis
import re
import json
import pymongo

from settings.local import redis_db, mongo_db

class MongoDB(object):
    def __init__(self, table):
        '''

        :param table: models中定义的表（models_obj.table）
        '''
        self.table = table

    def insert(self, data):
        '''

        :param data: 插入的数据字典
        :return: 成功返回自增id
        '''

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
        '''
       查询一条数据
        :param conditions: 查询的条件（字典）
        :param data: 显示指定的字段的字符串（不可以显示嵌套字典）
        :return: 查询结果的字典
        '''

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
        '''
        修改一条数据
        data的key为修改的字段，value为新值
        如果修改的是嵌套的内容，则修改的key用.链接
        例：{"roledata.nickSet": 1, "nick": name}
        :param conditions: 查询条件（字典）
        :param data: 更新的内容（字典）
        :param multi: 如果为True，修改查询到的所有数据
        :return: 
        '''
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
        '''
        删除符合条件的所有数据
        :param conditions: 查询条件
        :param multi: 如果等于True 删除所有数据
        '''

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
        '''
        查询返回的条数
        :param conditions: 查询条件的字典
        :return: int类型，没有返回0
        '''

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
    '''
    字符串
    '''
    def __init__(self, **kwargs):

        self.conn = redis.StrictRedis(**kwargs)

    def convert(self,data):
        '''
        :param data: bytes类型
        :return: str 类型
        如果传入的字典里面的key value是bytes，则可以递归将里面
        的所有bytes转换为str
        '''
        if isinstance(data, bytes):
            return data.decode('utf-8')
        if isinstance(data, dict):
            return dict(map(convert, data.items()))
        if isinstance(data, tuple):
            return map(convert, data)
        return data

    def json_format(self,data):
        '''
        :param data: redis数据库中取出的数据，或以 '包裹的类字典格式字符串
        :return: 标准的以"包裹的json字符串
        '''

        result = re.sub('\'', '\"', data)
        return result

    def conn(self):
        return self.conn

    def keys(self, key):
        '''
        :param key: key
        :return: 返回key的列表如果key为*，返回所有的key,没有查到返回空列表
        '''
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
        '''
               :param name: 哈希表名
               :param key: 哈希表的key
               :return: 成功True 失败 False
               '''
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
        '''
        :param key: key
        :param map: 字典
        :return: 成功True 失败 False
        '''
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
        '''
        :param key: key
        :return: key value对的个数
        '''
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
        '''
        :param key: key
        :return: 从头部取出一个元素
        '''
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
        '''
               :param key: key
               :return: 从头部取出一个元素
               '''
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

