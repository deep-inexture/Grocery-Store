from sqlalchemy.orm import Session
from .. import models
from sqlalchemy import and_


def view_products(db: Session):
    available_product = db.query(models.Product).all()
    return available_product


def search_by_name(name: str, db: Session):
    name_filter = db.query(models.Product).filter(models.Product.title.like(name+'%')).all()
    return name_filter


def search_by_price(max_price: float, min_price: float, db: Session):
    price_filter = db.query(models.Product).filter(models.Product.price > min_price, models.Product.price < max_price).all()
    return price_filter


def search_by_name_and_price(name: str, max_price: float, min_price: float, db: Session):
    name_and_price_filter = db.query(models.Product).filter(and_(and_(models.Product.price > min_price, models.Product.price < max_price), (models.Product.title.like(name+'%')))).all()
    return name_and_price_filter


def add_shipping_info(request, db: Session, email):
    uid = db.query(models.User.id).filter(models.User.email == email).first()
    new_address = models.ShippingInfo(
        name=request.name,
        phone_no=request.phone_no,
        address=request.address,
        city=request.city,
        state=request.state,
        user_id=uid[0]
    )
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address


def show_shipping_info(db, email):
    info = db.query(models.ShippingInfo).filter(and_(models.User.email == email, models.User.id == models.ShippingInfo.user_id)).all()
    return info
