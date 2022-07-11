from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import List
import datetime
from .. import models, schemas
from ..repository import messages

"""
This File does all validations related stuff to maintain routers to only route and keep file clean.
All Database query stuff also takes place here.
"""


def is_admin(email: str, db: Session):
    """
    Check isAdmin feature so that no user can access admin use cases.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In Admin Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: bool - Return True in only if admin is Logged-In
    """
    check_user = db.query(models.User).filter(models.User.email == email).first()
    if getattr(check_user, 'email') != 'admin@admin.in':
        return False
    return True


def all_products(db: Session, email):
    """
    Return all products details to verify after adding/updating.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In Admin Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Data as per Schema-Content
    """
    if not is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    return db.query(models.Product).order_by(asc(models.Product.id)).all()


def add_product(db: Session, request: List[schemas.ProductBase], email):
    """
    Add products to grocery via requested details.
    Parameters
    ----------------------------------------------------------
    request: Schemas Object - Add multiple Lists of data
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In Admin Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Status of Products added or not
    """
    if not is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    for items in request:
        new_item = models.Product(
            image_file=items.image_file,
            product_type=items.product_type,
            title=items.title,
            description=items.description,
            price=items.price,
            quantity=items.quantity
        )
        db.add(new_item)

    db.commit()
    return messages.json_status_response(200, "Items Added to the Grocery Store")


def update_product(item_id: int, db: Session, item: schemas.ProductBase, email):
    """
    Update items and their details as per requirements.
    Parameters
    ----------------------------------------------------------
    item_id: int - Product Item-ID
    item: schemas Object - Update item desc by item ID
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In Admin Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch updates made on products
    """
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
    check_item_id.product_type = item.product_type
    check_item_id.title = item.title
    check_item_id.description = item.description
    check_item_id.price = item.price
    check_item_id.quantity = item.quantity

    db.commit()
    return messages.json_status_response(200, "Items Updated Successfully.")


def delete_product(item_id: int, db: Session, email):
    """
    Delete products not needed in grocery with help of its id.
    Parameters
    ----------------------------------------------------------
    item_id: int - Product Item-ID
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In Admin Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Data that deleted
    """
    if not is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    delete_item = db.query(models.Product).filter(models.Product.id == item_id).first()
    if not delete_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.Product_Not_Found_404(item_id))

    db.delete(delete_item)
    db.commit()
    return messages.json_status_response(200, "Item Deleted from the Grocery Store")


def view_orders(db: Session, email):
    """
    View All Orders Details of User and status of Orders
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In Admin Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch All Data Available in Grocery
    """
    if not is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    return db.query(models.OrderDetails).order_by(desc(models.OrderDetails.id)).all()


def filter_order_status(request, db: Session, email):
    """
    Admin Filters all Order by its status
    Parameters
    ----------------------------------------------------------
    request: schemas Object - Update Order Status of user items
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch All Data Available in Grocery
    """
    if not is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    filtered_orders = db.query(models.OrderDetails).filter(models.OrderDetails.order_status == request.order_status).all()
    if not filtered_orders:
        raise HTTPException(status_code=404, detail=messages.RECORD_NOT_FOUND)
    return filtered_orders


def update_order_status(request, db, email):
    """
    Admin adds Discount Coupon and its records
    Parameters
    ----------------------------------------------------------
    request: schemas Object - Update Order Status of user items
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Updates Status as per its tracking flow.
    """
    if not is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    status_priority = ['received', 'packed', 'shipped', 'delivered', 'returned']
    find_order = db.query(models.OrderDetails).filter(models.OrderDetails.id == request.order_id).first()
    if not find_order:
        raise HTTPException(status_code=404, detail=messages.RECORD_NOT_FOUND)

    current_status = getattr(find_order, "order_status")
    if status_priority.index(request.order_status) <= status_priority.index(current_status):
        raise HTTPException(status_code=401, detail=messages.ORDER_PRIORITY_401)

    find_order.order_status = request.order_status
    db.commit()

    return messages.json_status_response(200, "Order Status Updated Successfully.")


def discount_coupon(db: Session, request: List[schemas.DiscountCoupon], email):
    """
    Add Discount Coupon and its records
    Parameters
    ----------------------------------------------------------
    request: schemas Object - Add multiple Discount coupons'
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In Admin Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Status of Coupons
    """
    if not is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    for coupon in request:
        if coupon.valid_till <= datetime.date.today().strftime("%Y-%m-%d"):
            raise HTTPException(status_code=401, detail=messages.INVALID_DATE_401)
        new_coupon = models.DiscountCoupon(
            coupon_code=coupon.coupon_code,
            discount_percentage=coupon.discount_percentage,
            valid_till=coupon.valid_till
        )
        db.add(new_coupon)

    db.commit()
    return messages.json_status_response(200, "Coupons Added Successfully")


def show_discount_coupon(db: Session, email):
    """
    Return all discount coupon details.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In Admin Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Data of all applicable coupons
    """
    if not is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    return db.query(models.DiscountCoupon).all()


def fetch_data(item_id: int, db: Session):
    """
    Common function to fetch data of products for other functions above.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    item_id: int - ID of product Item
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Data of all products with applicable ID
    """
    return db.query(models.Product).where(models.Product.id == item_id).first()
