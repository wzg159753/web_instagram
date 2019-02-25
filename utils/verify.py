import hashlib


def hash_md5(content):
    return hashlib.md5(content.encode('utf8')).hexdigest()

USER = {
    'username': 'too',
    'password': hash_md5('123')
}


def verify_login(username, password):
    """
    验证登录方法 对密码进行MD5比对
    :param username:
    :param password:
    :return:
    """
    if username and password:
        result = (username == USER['username']) and (hash_md5(password) == USER['password'])
        return result
    else:
        return False
