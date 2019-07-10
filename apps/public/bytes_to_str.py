

def convert(data):
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