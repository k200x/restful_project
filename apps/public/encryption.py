import hashlib

# 加密密码
def encryption(pw):
    m = hashlib.md5()
    password = 'sI+#!-ml%se'%pw
    m.update(password.encode('utf-8'))
    pw_md5 = m.hexdigest().upper()
    return pw_md5




if __name__ == '__main__':
    # a=encryption("crystal7")
    b=encryption("1234567")
    # c = "A47479A0D1775AD79A853F5CDE7BAF89"
    # d = "7709F2FA3C7DB8EC06D2DA97B40B5179"
    print("b",b)
    # print(b==d)
    # print(b)
    # print(a==c)
