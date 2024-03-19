# allows rating and reviewing of books
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False) # preferably use a 3-star rating
    review = Column(Text, nullable=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    book = relationship('Book', back_populates='reviews')
