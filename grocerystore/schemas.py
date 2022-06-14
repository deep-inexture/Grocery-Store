from pydantic import BaseModel
from typing import List, Optional

# Following File contains BaseModel for each table to make it visible in json format while building API's.'
# Each of them can be called as per requirements in response_model in routers.


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


class UserRegister(User):
    confirm_password: str

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

    class Config():
        orm_mode=True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
