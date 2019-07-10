def word_filter(key_list, user_input):
    """

    :param key_list: 屏蔽子列表
    :param user_input: 用户输入
    :return: 匹配成功返回>0的数，没有匹配返回-1
    """
    for key in key_list:

        if key in user_input and key != "":
            print("*"*100)
            print(key)
            print("*"*100)
            return True
    return False

