from pydantic import BaseModel
from typing import List, Optional


class ProductBase(BaseModel):
    image_file: str
    title: str
    description: str
    price: float
    quantity: int


class Product(ProductBase):
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