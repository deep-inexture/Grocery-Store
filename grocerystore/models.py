from grocerystore.database import Base
from sqlalchemy import String, Integer, Column, Float, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship

# This files stores schemas of tables like tableName, tableColumn, and its Datatype.
# Main file sees into this file first for each non created table to be generated or not.


class Product(Base):
    """This table contains elements required to identify different products and its stocks."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    image_file = Column(String(255), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False, unique=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)


class User(Base):
    """This Table has user details for authentication and access purpose."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

    shipping_info = relationship('ShippingInfo', back_populates="owner")
    my_cart = relationship('MyCart', back_populates="owner")
    order_details = relationship('OrderDetails', back_populates="owner")
    my_wallet = relationship('MyWallet', back_populates="owner")


class ResetCode(Base):
    """This table provides temporary token to reset user password if they forgot."""
    __tablename__ = "reset_codes"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True)
    reset_code = Column(String(50), nullable=False)
    status = Column(String(1), default=1)
    expired_in = Column(DateTime)


class ShippingInfo(Base):
    """This table provides address and contact details of user for shipment."""
    __tablename__ = "users_shipping_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=True)
    phone_no = Column(String(10), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="shipping_info")


class MyCart(Base):
    """This table has user products info that has been added to cart before payment and shipment"""
    __tablename__ = "my_cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    product_name = Column(String(255), nullable=False)
    product_quantity = Column(Integer, nullable=False)
    product_price = Column(Float, nullable=False)
    total = Column(Float, nullable=True)

    owner = relationship("User", back_populates="my_cart")


class OrderDetails(Base):
    """This Table has permanent records/ invoice details of user after successful process of payment."""
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    shipping_id = Column(Integer, ForeignKey('users_shipping_info.id'))
    description = Column(String(255), nullable=False)
    total_amount = Column(Float, nullable=False)
    payment_status = Column(String(50), default="pending")

    owner = relationship("User", back_populates="order_details")


class MyWallet(Base):
    """This Table Makes Record of Users Wallet Balance. """
    __tablename__ = "my_wallet"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    acc_balance = Column(Float, default=0)

    owner = relationship("User", back_populates="my_wallet")


class DiscountCoupon(Base):
    """Keeps Records of Discount Coupons."""
    __tablename__ = "discount_coupon"

    id = Column(Integer, primary_key=True, index=True)
    coupon_code = Column(String(20), nullable=False)
    discount_percentage = Column(Integer, nullable=False)
    valid_till = Column(Date)
    times_used = Column(Integer, default=0)