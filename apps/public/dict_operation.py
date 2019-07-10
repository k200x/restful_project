

# 返回两个相同key的字典value相加
def dic_val_sum(dic1,dic2):
    for k, v in dic1.items():
        if k in dic2.keys():
            dic2[k] += v
        else:
            dic2[k] = v
    return dic2



def dic_val_sum_set(dic_db,dic_new):
    for k, v in dic_new.items():

        if k.replace("set_","") in dic_db.keys():
            dic_db[k.replace("set_","")] += v
        else:
            dic_db[k.replace("set_","")] = v

    return dic_db



if __name__ == '__main__':
    # d1 = {"set_a":2,"set_b":{"c":5}} # 新数据
    # d2 = {"a":1,"b":{"c":2}} # 数据库中数据

    dic_new = {"set_a":10,"set_c":1}  # 新数据
    dic_db = {}  # 数据库中数据
    r = dic_val_sum_set(dic_db,dic_new)
    # result1 = dic_val_sum(d1["b"],d2["b"])# 先合并内层
    # print(result1)
    # del d1["b"]# 删除新数据中内层的数据
    # print(d1)
    # result2 = dic_val_sum(d1,d2)# 合并外层数据
    # print(result2)
    print(r)





