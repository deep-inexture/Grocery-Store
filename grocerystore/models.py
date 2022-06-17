from .database import Base
from sqlalchemy import String, Integer, Column, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# This files stores schemas of tables like tableName, tableColumn, and its Datatype.
# Main file sees into this file first for each non created table to be generated or not.


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    image_file = Column(String(255), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False, unique=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

    shipping_info = relationship('ShippingInfo', back_populates="owner")
    my_cart = relationship('MyCart', back_populates="owner")


class ResetCode(Base):
    __tablename__ = "reset_codes"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True)
    reset_code = Column(String(50), nullable=False)
    status = Column(String(1), default=1)
    expired_in = Column(DateTime)


class ShippingInfo(Base):
    __tablename__ = "users_shipping_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=True)
    phone_no = Column(Integer, nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="shipping_info")


class MyCart(Base):
    __tablename__ = "my_cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    product_name = Column(String(255), nullable=False)
    product_quantity = Column(Integer, nullable=False)
    product_price = Column(Float, nullable=False)
    status = Column(String(10), default="pending")

    owner = relationship("User", back_populates="my_cart")