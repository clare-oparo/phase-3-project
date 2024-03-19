# track reading goals
from sqlalchemy import Column, Integer, String, Date
from .base import Base

class ReadingGoal(Base):
    __tablename__ = 'reading goals'
    id = Column(Integer, primary_key=True)
    goal = Column(Integer, nullable=False) # number of books to read
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String, default='active') # add 'completed' and 'failed' as options