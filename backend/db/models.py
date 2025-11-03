from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class Test(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
