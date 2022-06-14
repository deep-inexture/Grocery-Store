from .database import Base
from sqlalchemy import String, Integer, Column, Float, Boolean

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
