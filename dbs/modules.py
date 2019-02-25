from datetime import datetime
from sqlalchemy import Column, Integer, String, DATETIME
from .connect import Base


class User(Base):
    """
    用户模型
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True,  autoincrement=True)
    username = Column(String(20), nullable=True, unique=True)
    password = Column(String(100), nullable=True)
    create_time = Column(DATETIME, default=datetime.now)

    def __repr__(self):
        return """
            <User>id={}, username={}, password={}, create_time={}
        """.format(
            self.id,
            self.username,
            self.password,
            self.create_time
        )