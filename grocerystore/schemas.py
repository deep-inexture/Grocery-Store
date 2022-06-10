from pydantic import BaseModel
from typing import List, Optional


class ProductBase(BaseModel):
    image_file: str = 'default.png'
    title: str = ''
    description: str = ''
    price: float = 0
    quantity: int = 0

    class Config():
        orm_mode=True


class Product(ProductBase):
    id: int

    class Config():
        orm_mode=True


class User(BaseModel):
    username: str
    email: str
    password: str

    class Config():
        orm_mode=True


class ShowUser(BaseModel):
    username: str
    email: str

    class Config():
        orm_mode=True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
