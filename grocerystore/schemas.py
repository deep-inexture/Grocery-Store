from pydantic import BaseModel
from typing import Optional, List

# Following File contains BaseModel for each table to make it visible in json format while building APIs.'
# Each of them can be called as per requirements in response_model in routers.


class ProductBase(BaseModel):
    """Admin UseCase: Fields required to create/Add Products"""
    image_file: str = 'default.png'
    title: str = ''
    description: str = ''
    price: float = 0
    quantity: int = 0

    class Conf:
        orm_mode = True


class Product(ProductBase):
    """Admin UseCase: id field inheriting from above class so that users can view and act accordingly"""
    id: int

    class Config:
        orm_mode = True


class User(BaseModel):
    """User UseCase: Registration Schema requirements for User"""
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True


class UserRegister(User):
    """User UseCase: Field required for users, but not needed in database. therefore different class
       via inheriting above class."""
    confirm_password: str

    class Config:
        orm_mode = True


class ShowUserBase(BaseModel):
    """User UseCase: Common Schema so that it can be viewed while accessing Foreign Key elements
        and values"""
    username: str
    email: str

    class Config:
        orm_mode = True


class ShowUser(ShowUserBase):
    """User UseCase: Schema that shows Shipping Info details including user details from Above."""
    shipping_info: List[ShowUserBase] = []

    class Config:
        orm_mode = True


class ShippingInfo(BaseModel):
    """User UseCase: Elements required while filling Shipping info."""
    name: str
    phone_no: int
    address: str
    city: str
    state: str

    class Config:
        orm_mode = True


class ShippingInfoBase(ShippingInfo):
    """User UseCase: Show owner details while accessing address details"""
    owner: ShowUserBase

    class Config:
        orm_mode = True


class MyCart(BaseModel):
    """User UseCase: Elements required for user to identify different products."""
    product_id: int
    product_name: str
    product_quantity: int
    product_price: float
    total: float

    class Config:
        orm_mode = True


class MyCartBase(MyCart):
    """User UseCase: Let user view their products with their own details """
    owner: ShowUserBase

    class Config:
        orm_mode = True


class AddToCart(BaseModel):
    """User UseCase: Fields user have to enter while adding products to cart."""
    item_id: int
    item_quantity: int

    class Config:
        orm_mode = True


class SearchProduct(BaseModel):
    """User UseCase: Optional fields for user to search products such as filter. """
    item_name: Optional[str] = ''
    max_price: Optional[float] = 1000
    min_price: Optional[float] = 0

    class Config:
        orm_mode = True


class Login(BaseModel):
    """User/Admin UseCase: Login Criteria to be fulfilled to access particular endpoints."""
    username: str
    password: str

    class Config:
        orm_mode = True


class OrderDetails(BaseModel):
    """Admin UseCase: View all order details in the records."""
    id: int
    user_id: int
    shipping_id: int
    description: str
    total_amount: float
    payment_status: str
    owner: ShowUserBase

    class Config:
        orm_mode = True


class Token(BaseModel):
    """User/Admin UseCase: Create Token and let user get their access_token for verification."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """User UseCase: for verifying above data email is mandatory to get user data."""
    email: Optional[str] = None


class ForgotPassword(BaseModel):
    """User UseCase: To recover password endpoint will require email to verify again."""
    email: str


class ResetPassword(BaseModel):
    """User UseCase: User will get again new token to recover password valid for some time."""
    token: str
    password: str
