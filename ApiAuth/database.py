from sqlalchemy import create_engine, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import ClassVar
from abc import ABCMeta

DATABASE_URL = "postgresql://postgres:Ziza97699778.@localhost/TeamUpUserAuth"



from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    

class UserLogin(BaseModel):
    username: str
    password: str


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    hashed_password = Column(String)


engine = create_engine(DATABASE_URL)

# Create the table
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()