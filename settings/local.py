# -*- coding: utf-8 -*-

from settings.conf_onoff import on_off_dic

conf = ""
for key in on_off_dic:
    if on_off_dic[key]:
        conf = key
        break



if conf == "online":

    # # 线上

    import logging
    # redis数据库配置

    redis_db = dict(

        # 线上redis
        host = "r-6we0c48d05d52304.redis.japan.rds.aliyuncs.com",
        port = 6379,
        password = "smilePassw0rd"

    )


    # mongodb 副本节点

    # 开启
    START = True

    CONN_ADDR1 = "dds-6wec0077d4c2afb41.mongodb.japan.rds.aliyuncs.com:3717"
    CONN_ADDR2 = "dds-6wec0077d4c2afb42.mongodb.japan.rds.aliyuncs.com:3717"
    REPLICAT_SET = ''
    username = 'root'
    password = 'smilePassw0rd'
    port = 27017



    mongo_db = dict(
        host="172.24.39.239",
        port=27017,
    )

# =========================
if conf == "dev":
    ## 开发

    # redis数据库配置

    redis_db = dict(
        # 本地测试redis
        host = "127.0.0.1",
        port = 6379,

    )

    # mongodb 副本节点

    # 开启
    START = False

    CONN_ADDR1 = "dds-2ze3a9b84da79c841.mongodb.rds.aliyuncs.com:3717"
    CONN_ADDR2 = "dds-2ze3a9b84da79c842.mongodb.rds.aliyuncs.com:3717"
    REPLICAT_SET = 'mgset-4403913'
    username = 'root'
    password = 'smilePassw0rd'
    port = 27017

    mongo_db = dict(
        host="127.0.0.1",
        port=27017,
    )

if conf == "local":

    ## 本地

    # redis数据库配置

    redis_db = dict(
        # 本地测试redis
        host = "127.0.0.1",
        port = 6379,

    )


    # mongodb 副本节点

    # 开启
    START = False

    CONN_ADDR1 = "dds-2ze3a9b84da79c841.mongodb.rds.aliyuncs.com:3717"
    CONN_ADDR2 = "dds-2ze3a9b84da79c842.mongodb.rds.aliyuncs.com:3717"
    REPLICAT_SET = 'mgset-4403913'
    username = 'root'
    password = 'smilePassw0rd'
    port = 27017



    mongo_db = dict(
        host="0.0.0.0",
        port=27017,
    )

if conf == "test":
    ## 测试服

    # redis数据库配置

    redis_db = dict(
        # 本地测试redis
        host="localhost",
        port=6379,

    )

    # mongodb 副本节点

    # 开启
    START = False

    CONN_ADDR1 = "dds-2ze3a9b84da79c841.mongodb.rds.aliyuncs.com:3717"
    CONN_ADDR2 = "dds-2ze3a9b84da79c842.mongodb.rds.aliyuncs.com:3717"
    REPLICAT_SET = 'mgset-4403913'
    username = 'root'
    password = 'smilePassw0rd'
    port = 27017

    mongo_db = dict(
        host="0.0.0.0",
        port=27017,
    )

if conf == "tw_ts":
    ## 开发

    # redis数据库配置

    redis_db = dict(
        # 本地测试redis
        host = "127.0.0.1",
        port = 6379
    )


    # mongodb 副本节点

    # 开启
    START = False

    CONN_ADDR1 = "dds-2ze3a9b84da79c841.mongodb.rds.aliyuncs.com:3717"
    CONN_ADDR2 = "dds-2ze3a9b84da79c842.mongodb.rds.aliyuncs.com:3717"
    REPLICAT_SET = 'mgset-4403913'
    username = 'root'
    password = 'smilePassw0rd'
    port = 27017

    mongo_db = dict(
        host="127.0.0.1",
        port=27017,
    )



