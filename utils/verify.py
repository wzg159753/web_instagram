import os

import hashlib
from dbs.modules import User, session, Post, Like, exists, Atte
from sqlalchemy_pagination import paginate


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
        info = {'status': 200, 'msg': '/'}
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




def paginations(page):
    """
    sqlalchemy_pagination 的分页库
    :param page:
    :return:
    """
    # 第一个参数传入post的个数 ， 第二个参数是页数， 第三个参数是一页多少个
    return paginate(Post.get_posts(), int(page), 4)





def add_like(user_id, post_id):
    """
    添加喜欢
    :param user_id:
    :param post_id:
    :return:
    """
    info = Like(user_id=user_id, post_id=post_id)
    session.add(Like(user_id=user_id, post_id=post_id))
    session.commit()
    return True

def get_user_likes(username):
    """
    获取用户喜欢的图片
    :return: post喜欢List
    """
    user = get_user(username)
    if user:
        # 返回所有喜欢的post信息  对应的用户喜欢的图片  返回列表
        like_posts = session.query(Post).filter(Post.id == Like.post_id, user.id == Like.user_id, Like.user_id != Post.user_id).all() # 自己上传的不能喜欢
        return like_posts

def is_like_exits(user_id, post_id):
    """
    判断这张图片 该用户是否已经喜欢
    :param user_id:
    :param post_id:
    :return:
    """
    return session.query(Like).filter(Like.user_id == user_id, Like.post_id == post_id).first()

def delete_like(user_id, post_id):
    """
    删除这条喜欢
    :param user_id:
    :param post_id:
    :return:
    """
    info = session.query(Like).filter(Like.user_id == user_id, Like.post_id == post_id).first()
    session.delete(info)
    session.commit()

def count_like(post_id):
    """
    统计喜欢人数
    :param post_id:
    :return:
    """
    return session.query(Like).filter(Like.post_id == post_id).count()




def is_atte_exits(m_id, y_id):
    """
    判断用户是否已经关注
    :param m_id:
    :param y_id:
    :return:
    """
    return session.query(Atte).filter(Atte.m_id == m_id, Atte.y_id == y_id).first()

def add_atte_prople(m_id, y_id):
    """
    添加用户关注
    :param m_id: 关注人id
    :param y_id: 被关注人id
    :return:
    """
    session.add(Atte(m_id=m_id, y_id=y_id))
    session.commit()

def delete_atte(m_id, y_id):
    """
    取消关注
    :param m_id: 关注人id
    :param y_id: 被关注人id
    :return:
    """
    info = session.query(Atte).filter(Atte.m_id == m_id, Atte.y_id == y_id).first()
    session.delete(info)
    session.commit()




def get_post(u_id, p_id):
    """
    获取post信息
    :param u_id:
    :param p_id:
    :return:
    """
    return session.query(Post).filter(Post.user_id == u_id, Post.id == p_id).first()

def delete_upload_img(u_id, p_id):
    """
    删除用户自己上传的图片
    :param u_id: 用户id
    :param p_id: 图片id
    :return:
    """
    post = get_post(u_id, p_id)
    os.remove(os.path.join('static', post.img_url))
    os.remove(os.path.join('static', post.thumb_url))
    session.execute('DELETE FROM posts WHERE id={} AND user_id={}'.format(p_id, u_id))
    session.commit()



