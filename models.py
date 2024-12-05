from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  # Unique username
    email = Column(String, unique=True, index=True)     # Unique email
    hashed_password = Column(String)  # Storing hashed password