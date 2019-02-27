import hashlib
from dbs.modules import User, session, Post


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

def user_add(username, password, sex):
    info = {}
    if not User.is_exits_user(username):
        User.add_user(username, password, sex)
        info['msg'] = '/'
        return info
    else:
        info['msg'] = 'final'
        return info

def get_user(username):
    return session.query(User).filter(User.username == username).first()

def add_post_for(img_url, thumb_url, user):
    user = get_user(user)
    post = Post(img_url=img_url, thumb_url=thumb_url, user_id=user.id)
    if post:
        session.add(post)
        session.commit()
        return post
    else:
        return '0'

def get_post_all():
    return session.query(Post).all()

def get_upload_post(username):
    user = get_user(username)
    return session.query(Post).filter(Post.user_id == user.id).all()

def get_post_id(post_id):
    return session.query(Post).filter(Post.id == post_id).first()