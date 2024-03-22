# allows rating and reviewing of books
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    rating = Column(Integer, nullable=False) 
    review = Column(Text, nullable=True)
    #notes = Column(Text, nullable=True)
    book = relationship('Book', back_populates='reviews')
