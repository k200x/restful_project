
import re

def json_format(data):
    '''
    :param data: redis数据库中取出的数据，或以 '包裹的类字典格式字符串
    :return: 标准的以"包裹的json字符串
    '''
    result = re.sub('\'', '\"', data)
    return result