from datetime import date

from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(..., max_length=16)
    email: EmailStr
    password: str = Field(..., min_length=8,
                               max_length=16)

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    register_date: date

    class Config:
        orm_mode = True

class UserSearch(BaseModel):
    username: str = Field(..., max_length=16)

class UserUpdatePassword(BaseModel):
    id: int
    password: str = Field(..., min_length=8,
                               max_length=16)

class UserDelete(BaseModel):
    id: int
