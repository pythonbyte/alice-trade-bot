"""File responsible to handle the connection with db and Models."""
import os
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Any
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "alice.db")

engine = create_engine(f'sqlite:///{DB_PATH}')
Session = sessionmaker(bind=engine)

Base: Any = declarative_base()

class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    action = Column(String)
    symbol = Column(String)
    shares = Column(Integer)
    price = Column(Integer)


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    platform = Column(String)
    token = Column(String)
