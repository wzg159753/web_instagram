from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


USER = 'admin'
PASSWORD = 'Root110qwe'
HOST = '192.168.35.128'
PORT = '3306'
DBS = 'tornado25'

db_url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USER,
    PASSWORD,
    HOST,
    PORT,
    DBS
)

engine = create_engine(db_url)
Base = declarative_base(engine)
Session = sessionmaker(engine)

if __name__ == '__main__':
    cursor = engine.connect()
    result = cursor.execute('select 1')
    print(result.fetchone())