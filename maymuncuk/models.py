from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
 

class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    query = Column(String(128), nullable=False)
    date = Column(Date(), nullable=False)
    clicks = Column(Float(), nullable=False)
    impressions = Column(Float(), nullable=False)
    ctr = Column(Float(), nullable=False)
    position = Column(Float(), nullable=False)