from datetime import datetime
from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey
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
        info = User(username=username, password=password, sex=sex)
        session.add(info)
        session.commit()
        return True

    @classmethod
    def is_exits_user(cls, username):
        return session.query(exists().where(User.username == username)).scalar()

    @classmethod
    def get_user(cls, username):
        return session.query(User).filter(User.username == username).first()


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