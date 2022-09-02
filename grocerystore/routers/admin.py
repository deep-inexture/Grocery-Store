from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from fastapi_pagination import Page, add_pagination, paginate, Params
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
def all_products(params: Params = Depends(), db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    FETCH ALL PRODUCTS AVAILABLE IN GROCERY
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    current_user: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Data as per Schema-Content
    """
    return paginate(admin.all_products(db, current_user.email), params)


@router.post("/create_items", status_code=status.HTTP_201_CREATED)
def add_product(request: List[schemas.ProductBase], db: Session = Depends(get_db),
                current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    ADD PRODUCTS TO SHOW IN GROCERY
    Parameters
    ----------------------------------------------------------
    request: Schemas Object - Add multiple Lists of data
    db: Database Object - Fetching Schemas Content
    current_user: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Status of Products added or not
    """
    admin.add_product(db, request, current_user.email)
    return {'DB Status': 'Item Added Successfully'}


@router.put("/update_item/{item_id}", status_code=status.HTTP_200_OK)
def update_product(item_id: int, item: schemas.ProductBase, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    UPDATE PRODUCTS FOR GROCERY
    Parameters
    ----------------------------------------------------------
    item_id: int - Product Item-ID
    item: schemas Object - Update item desc by item ID
    db: Database Object - Fetching Schemas Content
    current_user: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch updates made on products
    """
    return admin.update_product(item_id, db, item, current_user.email)


@router.delete("/delete_item/{item_id}", status_code=status.HTTP_200_OK)
def delete_product(item_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    DELETE ITEMS NOT IN GROCERY
    Parameters
    ----------------------------------------------------------
    item_id: int - Product Item-ID
    db: Database Object - Fetching Schemas Content
    current_user: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Data that deleted
    """
    return admin.delete_product(item_id, db, current_user.email)


@router.get("/view_orders", summary="View all Order Details by each User", response_model=Page[schemas.OrderDetails])
def view_orders(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    FETCH ALL ORDERS PLACED BY USER AND CHECK ORDER STATUS
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    current_user: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch All Data Available in Grocery
    """
    return paginate(admin.view_orders(db, current_user.email))


@router.post("/filter_order_status", summary="Filter the order Status By Order Status", response_model=Page[schemas.OrderDetails])
def filter_order_status(request: schemas.FilterOrderStatus, db: Session = Depends(get_db),
                        current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
        Admin Filters all Order by its status
        Parameters
        ----------------------------------------------------------
        request: schemas Object - Update Order Status of user items
        db: Database Object - Fetching Schemas Content
        current_user: User Object - Current Logged-In User Session
        ----------------------------------------------------------

        Returns
        ----------------------------------------------------------
        response: json object - Updates Status as per its tracking flow.
        """
    return paginate(admin.filter_order_status(request, db, current_user.email))


@router.put("/update_order_status", summary="Update the order Status for tracking purpose", status_code=status.HTTP_200_OK)
def update_order_status(request: schemas.OrderStatus, db: Session = Depends(get_db),
                        current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
        Admin Updates Order Status as per its tracking system
        Parameters
        ----------------------------------------------------------
        request: schemas Object - Update Order Status of user items
        db: Database Object - Fetching Schemas Content
        current_user: User Object - Current Logged-In User Session
        ----------------------------------------------------------

        Returns
        ----------------------------------------------------------
        response: json object - Updates Status as per its tracking flow.
        """
    return admin.update_order_status(request, db, current_user.email)


@router.post("/add_discount_coupon", summary="Add Discount Coupons for Users", status_code=status.HTTP_201_CREATED)
def add_discount_coupon(request: List[schemas.DiscountCoupon], db: Session = Depends(get_db),
                        current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Admin adds Discount Coupon and its records
    Parameters
    ----------------------------------------------------------
    request: schemas Object - Add multiple Discount coupons'
    db: Database Object - Fetching Schemas Content
    current_user: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Status of Coupons
    """
    return admin.discount_coupon(db, request, current_user.email)


@router.get("/show_discount_coupon")
def show_discount_coupon(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Get All the Discount Coupons Visible.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    current_user: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Data of all applicable coupons
    """
    return admin.show_discount_coupon(db, current_user.email)


add_pagination(router)
