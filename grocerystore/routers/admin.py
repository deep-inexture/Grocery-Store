from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from fastapi_pagination import Page, add_pagination, paginate, LimitOffsetPage
from .. import database, schemas, oauth2
from ..repository import admin

"""
This File Contains all Admin Related Routes such as ADD | UPDATE | DELETE Products and many more.
All validations and query gets fired in other file with same name in repository directory.
"""


router = APIRouter(
    tags=["Admin"],
    prefix="/admin"
)
get_db = database.get_db


@router.get("/get_items", response_model=Page[schemas.Product])
def all_products(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    FETCH ALL PRODUCTS AVAILABLE IN GROCERY
    """
    return paginate(admin.all_products(db, current_user.email))


@router.post("/create_items", status_code=status.HTTP_201_CREATED)
def add_product(request: List[schemas.ProductBase], db: Session = Depends(get_db),
                current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    ADD PRODUCTS TO SHOW IN GROCERY
    """
    admin.add_product(db, request, current_user.email)
    return {'DB Status': 'Item Added Successfully'}


@router.put("/update_item/{item_id}", status_code=status.HTTP_200_OK)
def update_product(item_id: int, item: schemas.ProductBase, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    UPDATE PRODUCTS FOR GROCERY
    """
    return admin.update_product(item_id, db, item, current_user.email)


@router.delete("/delete_item/{item_id}", status_code=status.HTTP_200_OK)
def delete_product(item_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    DELETE ITEMS NOT IN GROCERY
    """
    return admin.delete_product(item_id, db, current_user.email)


@router.get("/view_orders", summary="View all Order Details by each User", response_model=List[schemas.OrderDetails])
def view_orders(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    FETCH ALL ORDERS PLACED BY USER AND CHECK ORDER STATUS
    """
    return admin.view_orders(db, current_user.email)


@router.post("/add_discount_coupon", summary="Add Discount Coupons for Users", status_code=status.HTTP_201_CREATED)
def add_discount_coupon(request: List[schemas.DiscountCoupon], db: Session = Depends(get_db),
                        current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Admin adds Discount Coupon and its records
    """
    return admin.discount_coupon(db, request, current_user.email)


@router.get("/show_discount_coupon")
def show_discount_coupon(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Get All the Discount Coupons Visible.
    """
    return admin.show_discount_coupon(db, current_user.email)


add_pagination(router)
