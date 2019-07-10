
# 配置文件开关
#
# on_off_dic = {
#     "online":False,
#     "dev":False,
#     "mac":True
# }

local_list = ["10.0.7.142"]  # 本地
dev_list = ["39.108.106.109"]  # 开发机
test_list = ["10.10.179.3"]  # 测试机
online_list = ["172.24.39.233", "172.24.39.232", "47.245.29.252", "47.245.30.61"]  # 台湾线上

tw_ts_list = ["10.0.0.179"]

def getIp():
    import socket
    myname = socket.getfqdn(socket.gethostname())
    try:
        myaddr = socket.gethostbyname(myname)
    except socket.gaierror:
        myaddr = "10.0.7.142"
    return myaddr

def main():
    ip = getIp()
    print(ip)
    on_off_dic = {
            "online":False,
            "dev":False,
            "test":False,
            "local":True,
            "tw_ts":False
            }
    if ip in dev_list:
        on_off_dic = {
            "online":False,
            "dev":True,
            "test": False,
            "local":False,
            "tw_ts": False
            }
    elif ip in test_list:
        on_off_dic = {
            "online": False,
            "dev": False,
            "test": True,
            "local": False,
            "tw_ts": False
        }
    elif ip in online_list:
        on_off_dic = {
            "online": True,
            "dev": False,
            "test": False,
            "local": False,
            "tw_ts": False
        }
    elif ip in local_list:
        on_off_dic = {
            "online": False,
            "dev": False,
            "test": False,
            "local": True,
            "tw_ts": False
        }
    elif ip in tw_ts_list:
        on_off_dic = {
            "online": False,
            "dev": False,
            "test": False,
            "local": False,
            "tw_ts": True
        }

    return on_off_dic

on_off_dic = main()
