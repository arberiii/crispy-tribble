import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Block(Base):
    __tablename__ = 'blocks'

    height = Column(Integer, primary_key=True)
    hash = Column(String, unique=True)
    timestamp = Column(DateTime)
    transactions = relationship("Transaction", back_populates="block")

class Transaction(Base):
    __tablename__ = 'transactions'

    txid = Column(String, primary_key=True)
    block_height = Column(Integer, ForeignKey('blocks.height'))
    block = relationship("Block", back_populates="transactions")
    timestamp = Column(DateTime)
    fee = Column(Float)
    size = Column(Integer)

class Input(Base):
    __tablename__ = 'inputs'

    id = Column(Integer, primary_key=True)
    txid = Column(String)
    vout = Column(Integer)

class Output(Base):
    __tablename__ = 'outputs'

    id = Column(Integer, primary_key=True)
    txid = Column(String)
    n = Column(Integer)
    value = Column(Float)
    address = Column(String)

def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)() 