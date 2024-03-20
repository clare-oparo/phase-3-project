# from sqlalchemy import Column, Integer, Text, ForeignKey
# from sqlalchemy.orm import relationship
# from .base import Base 

# class Note(Base):
#     __tablename__ = 'notes'
#     id = Column(Integer, primary_key=True)
#     content = Column(Text, nullable=False)
#     book_id = Column(Integer, ForeignKey('books.id'), nullable=False)

#     book = relationship('Book', back_populates='notes')