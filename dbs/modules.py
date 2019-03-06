from datetime import datetime
from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey, Table
from .connect import Base, Session
from sqlalchemy.orm import relationship
from sqlalchemy.sql import exists

session = Session()

class User(Base):
    """
    用户模型
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True,  autoincrement=True)
    username = Column(String(20), nullable=True, unique=True)
    password = Column(String(100), nullable=True)
    create_time = Column(DATETIME, default=datetime.now)
    sex = Column(String(10))
    posts = relationship('Post', back_populates='users')

    def __repr__(self):
        return """
            <User>id={}, username={}, password={}, create_time={}
        """.format(
            self.id,
            self.username,
            self.password,
            self.create_time
        )

    @classmethod
    def add_user(cls, username, password, sex):
        """
        添加用户方法
        :param username:
        :param password:
        :param sex:
        :return:
        """
        info = User(username=username, password=password, sex=sex)
        session.add(info)
        session.commit()
        return True

    @classmethod
    def is_exits_user(cls, username):
        """
        判断用户名存不存在方法
        :param username:
        :return:
        """
        return session.query(exists().where(User.username == username)).scalar()

    @classmethod
    def get_user(cls, username):
        """
        获取用户方法
        :param username:
        :return:
        """
        return session.query(User).filter(User.username == username).first()

    @classmethod
    def get_user_info(cls, username, password):
        """
        判断用户信息方法  主要是后台password的比对
        :param username:
        :param password:
        :return:
        """
        return session.query(User).filter(User.username == username, User.password == password).first()


class Post(Base):
    """
    Post 用户上传的图片信息模型
    """
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    img_url = Column(String(200), nullable=True)
    thumb_url = Column(String(200), nullable=True)
    create_time = Column(DATETIME, default=datetime.now)
    user_id = Column(Integer, ForeignKey('user.id'))
    users = relationship('User', back_populates='posts')

    @classmethod
    def get_posts(cls):
        """
        用于分页的方法  注意分页只能作用对象
        :return:
        """
        return session.query(Post).order_by(Post.id.desc())


class Like(Base):
    """
    创建Like 用户喜欢模型
    """
    __tablename__ = 'likes'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    create_time = Column(DATETIME, default=datetime.now)


class Atte(Base):
    """
    建立用户关注表
    """
    __tablename__ = 'attes'
    # 关注人
    m_id = Column(Integer, ForeignKey('user.id'), primary_key=True) # 关注用户
    # 被关注人
    y_id = Column(Integer, ForeignKey('user.id'), primary_key=True) # 被关注

    def __repr__(self):
        return '''
            <Atte>++m_id={}, y_id={}
        '''.format(
            self.m_id,
            self.y_id
        )