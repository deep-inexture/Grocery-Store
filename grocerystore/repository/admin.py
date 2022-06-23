from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from . import messages
from typing import List

# This File does all validations related stuff to maintain routers to only route and keep file clean.
# All Database query stuff also takes place here.


def is_admin(email: str, db: Session):
    """Check isAdmin feature so that no user can access admin use cases."""
    check_user = db.query(models.User).filter(models.User.email == email).first()
    if getattr(check_user, 'email') != 'admin@admin.in':
        return False
    return True


def all_products(db: Session):
    """Return all products details to verify after adding/updating."""
    return db.query(models.Product).all()


def add_product(db: Session, request: List[schemas.ProductBase], email):
    """Add products to grocery via requested details."""
    if not is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    for items in request:
        new_item = models.Product(
            image_file=items.image_file,
            title=items.title,
            description=items.description,
            price=items.price,
            quantity=items.quantity
        )
        db.add(new_item)

    db.commit()
    return {'status': 'Done'}


def update_product(item_id: int, db: Session, item: schemas.ProductBase, email):
    """Update items and their details as per requirements."""
    if not is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    check_item_id = db.query(models.Product).filter(models.Product.id == item_id).first()
    if not check_item_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.Product_Not_Found_404(item_id))

    items_found = fetch_data(item_id, db)
    image_file = getattr(items_found, 'image_file')
    title = getattr(items_found, 'title')
    description = getattr(items_found, 'description')
    price = getattr(items_found, 'price')
    quantity = getattr(items_found, 'quantity')

    if image_file == item.image_file and title == item.title and description == item.description and price == item.price and quantity == item.quantity:
        raise HTTPException(status_code=302, detail=messages.NO_CHANGES_302)

    check_item_id.image_file = item.image_file
    check_item_id.title = item.title
    check_item_id.description = item.description
    check_item_id.price = item.price
    check_item_id.quantity = item.quantity

    db.commit()
    return {f"Product Image =       {image_file}": f"changed to {check_item_id.image_file}",
            f"Product Title =       {title}": f"changed to {check_item_id.title}",
            f"Product Description = {description}": f"changed to {check_item_id.description}",
            f"Product Price =       {price}": f"changed to {check_item_id.price}",
            f"Product Quantity =    {quantity}": f"changed to {check_item_id.quantity}"}


def delete_product(item_id: int, db: Session, email):
    """Delete products not needed in grocery with help of its id."""
    if not is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    delete_item = db.query(models.Product).filter(models.Product.id == item_id).first()
    if not delete_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.Product_Not_Found_404(item_id))
    items_found = fetch_data(item_id, db)
    title = getattr(items_found, 'title')
    db.delete(delete_item)
    db.commit()
    return {f"Product {title}": "Deleted Successfully"}


def view_orders(db: Session, email):
    """View All Orders Details of User and status of Orders"""
    if not is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    return db.query(models.OrderDetails).all()


def fetch_data(item_id: int, db: Session):
    """Common function to fetch data of products for other functions above."""
    return db.query(models.Product).where(models.Product.id == item_id).first()
