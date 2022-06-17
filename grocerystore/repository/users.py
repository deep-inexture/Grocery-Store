from sqlalchemy.orm import Session
from fastapi import HTTPException, status
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


def add_to_cart(request, db: Session, email):
    uid = db.query(models.User.id).filter(models.User.email == email).first()
    pid = db.query(models.Product).filter(models.Product.id == request.item_id).first()

    """Check Product Exists or Not"""
    if not pid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with {request.item_id} Not Exists.")

    stock_id = getattr(pid, "id")
    stock_quantity = getattr(pid, "quantity")
    stock_title = getattr(pid, "title")
    stock_price = getattr(pid, "price")

    """Check Product Availability."""
    if request.item_quantity > getattr(pid, "quantity"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Stock UnAvailable! {stock_quantity} Stocks left.")

    """Add Product Details to MyCart."""
    cart_item = models.MyCart(
        user_id=uid[0],
        product_id=stock_id,
        product_name=stock_title,
        product_quantity=stock_quantity,
        product_price=stock_price
    )
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return {"Status": "Item Added to your Cart"}


def my_cart(db: Session, email):
    uid = db.query(models.User.id).filter(models.User.email == email).first()
    my_products = db.query(models.MyCart).filter(models.MyCart.user_id == uid[0]).all()
    return my_products


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
