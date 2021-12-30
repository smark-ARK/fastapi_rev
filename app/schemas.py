from datetime import datetime
from typing import List
from pydantic import BaseModel
from pydantic.networks import EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str  # to hash


class UUser(BaseModel):
    username: str
    email: EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    image_url: str
    url_type: str


class Post(PostBase):
    class Config:
        orm_mode = True

    pass


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    posts: List[Post]

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    image_url: str
    url_type: str
    user: UserOut

    class Config:
        orm_mode = True


class PostUpdate(PostBase):
    pass


class AuthRequest(BaseModel):
    email: EmailStr
    password: str
