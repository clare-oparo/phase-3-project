# track info on books
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from .base import Base

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String)
    total_pages = Column(Integer)
    status = Column(String, default='unread') #options are unread, in progress and complete
    current_page = Column(Integer, default=0)
    #define review model!
    reviews = relationship('Review', back_populates='book')