from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from typing import List


def view_products(db: Session):
    available_product = db.query(models.Product).all()
    return available_product


def search_by_name(name: str, db: Session):
    name_filter = db.query(models.Product).filter(models.Product.title.like(name)).all()
    return name_filter


# def search_by_price(max_price: float, min_price: float, db: Session):
#     price_filter = db.query(models.Product).where(models.Product.price == max_price)
#     # print(price_filter)
#     # print(getattr(price_filter, 'price'))
#     return price_filter
