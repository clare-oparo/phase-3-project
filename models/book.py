# track info on books
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy.ext.hybrid import hybrid_property


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String)
    total_pages = Column(Integer)
    current_page = Column(Integer)
    status = Column(String, nullable=False) # options are unread, in progress and complete
    reviews = relationship('Review', back_populates='book', cascade='all, delete-orphan')
    

    # one book can have many notes
    # notes = relationship('Note', back_populates='book')
   

    @property 
    def progress(self):
        '''Calculate reading progress as a percentage'''
        if not self.total_pages or self.total_pages == 0:
            return 0
        return (self.current_page / self.total_pages) * 100
    
    @progress.setter
    def progress(self, value):
        if 0 <= value <= 100:
            self.current_page = round((value / 100) * self.total_pages)

    @hybrid_property
    def status(self):
        if self.current_page <= 0:
            return 'unread'
        elif self.current_page == self.total_pages:
            return 'complete'
        else:
            return 'in progress'
    
    @status.setter
    def status(self, value):
        pass