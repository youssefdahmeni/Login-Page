from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, EmailStr

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)  # Added length constraint
    email = Column(String(100), unique=True, index=True)    # Added length constraint
    hashed_password = Column(String(100))                   # Added length constraint

# Pydantic models for request/response
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserInDB(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str

    class Config:
        from_attributes = True  # Updated for Pydantic v2 compatibility

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True  # Updated for Pydantic v2 compatibility