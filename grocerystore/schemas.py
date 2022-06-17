from pydantic import BaseModel
from typing import Optional, List

# Following File contains BaseModel for each table to make it visible in json format while building APIs.'
# Each of them can be called as per requirements in response_model in routers.


class ProductBase(BaseModel):
    image_file: str = 'default.png'
    title: str = ''
    description: str = ''
    price: float = 0
    quantity: int = 0

    class Config():
        orm_mode = True


class Product(ProductBase):
    id: int

    class Config():
        orm_mode = True


class User(BaseModel):
    username: str
    email: str
    password: str

    class Config():
        orm_mode = True


class UserRegister(User):
    confirm_password: str

    class Config():
        orm_mode = True


class ShowUserBase(BaseModel):
    username: str
    email: str

    class Config():
        orm_mode = True


class ShowUser(ShowUserBase):
    shipping_info: List[ShowUserBase] = []

    class Config():
        orm_mode = True


class ShippingInfo(BaseModel):
    name: str
    phone_no: int
    address: str
    city: str
    state: str

    class Config():
        orm_mode = True


class ShippingInfoBase(ShippingInfo):
    owner: ShowUserBase

    class Config():
        orm_mode = True


class MyCart(BaseModel):
    product_name: str
    product_quantity: int
    product_price: float
    status: str

    class Config():
        orm_mode = True


class MyCartBase(MyCart):
    owner: ShowUserBase

    class Config():
        orm_mode = True


class AddToCart(BaseModel):
    item_id: int
    item_quantity: int

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str

    class Config():
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class ForgotPassword(BaseModel):
    email: str


class ResetPassword(BaseModel):
    token: str
    password: str