import hashlib
from dbs.modules import User, session, Post


def hash_md5(content):
    """
    对密码进行MD5加密
    :param content:
    :return:
    """
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
        # 调用modules中的User的类方法验证通过
        result = User.get_user_info(username, hash_md5(password))
        return result
    else:
        return False

def signup_user(username, password, sex):
    """
    注册用户 判断这个用户名存不存在 如果存在就 输出msg
    :param username:
    :param password:
    :param sex:
    :return:
    """
    info = {}
    if not User.is_exits_user(username):
        # 如果不存在  就注册
        User.add_user(username, hash_md5(password), sex)
        info = {'status': 200, 'msg': 'ok'}
        return info
    else:
        info = {'status': 400, 'msg': 'error'}
        return info

def get_user(username):
    """
    获取用户
    :param username:
    :return:
    """
    return session.query(User).filter(User.username == username).first()

def add_post_for(img_url, thumb_url, user):
    """
    将图片路径信息保存到数据库
    :param img_url:
    :param thumb_url:
    :param user:
    :return:
    """
    user = get_user(user)
    post = Post(img_url=img_url, thumb_url=thumb_url, user_id=user.id)
    if post:
        session.add(post)
        session.commit()
        # 返回这个实例  供图片跳转
        return post
    else:
        return '0'

def get_post_all():
    """
    获取所有post的路径信息 展示explore页面
    :return:
    """
    return session.query(Post).order_by(Post.id.desc()).all()

def get_upload_post(username):
    """
    获取上传的图片  展示Index页面
    :param username:
    :return:
    """
    user = get_user(username)
    if user:
        return session.query(Post).filter(Post.user_id == user.id).order_by(Post.id.desc()).all()

def get_post_id(post_id):
    """
    获取post的id那条数据
    :param post_id:
    :return:
    """
    return session.query(Post).filter(Post.id == post_id).first()