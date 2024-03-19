from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base import Base

DATABASE_URI = 'sqlite:///liblog.db'

def init_db():
    engine = create_engine(DATABASE_URI, echo=True)
    Base.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine))

if __name__ == '__main__':
    init_db()
    print('Database successfully initialized.')