from .database import Base
from sqlalchemy import String, Integer, Boolean, Text, Column, Float


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