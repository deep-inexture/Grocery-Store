from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, schemas, oauth2
from sqlalchemy.orm import Session
from typing import List
from ..repository import users, admin
from fastapi_pagination import Page, add_pagination, paginate, LimitOffsetPage

router = APIRouter(
    tags=["User"],
    prefix="/user"
)

get_db = database.get_db


@router.get("/view_products", response_model=Page[schemas.Product])
@router.get("/view_products/limit-offset", response_model=LimitOffsetPage[schemas.Product])
def view_products(db: Session = Depends(get_db)):
    """
    Any User has access to view all the products available in grocery db.
    """
    return paginate(users.view_products(db))
add_pagination(router)


@router.post("/search_products", response_model=List[schemas.Product])
def search_products(request: schemas.SearchProduct, db: Session = Depends(get_db)):
    """
    Search Filters to make easy access to required Products.
    """
    name_and_price = users.search_by_name_and_price(request, db)
    if not name_and_price:
        raise HTTPException(status_code=404, detail=f"No Records Found!!!")
    return name_and_price


@router.post("/add_to_cart", status_code=status.HTTP_200_OK)
def add_to_cart(request: schemas.AddToCart, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Add your favorite Item to your Cart by entering item id from view products/ search products.
    """
    if admin.is_admin(current_user.email, db):
        raise HTTPException(status_code=401, detail=f"You are not Authorized to view this Page!")
    return users.add_to_cart(request, db, current_user.email)


@router.get("/view_my_cart", response_model=List[schemas.MyCartBase])
def my_cart(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    User can view their Cart and their Products Added to cart
    """
    if admin.is_admin(current_user.email, db):
        raise HTTPException(status_code=401, detail=f"You are not Authorized to view this Page!")
    return users.my_cart(db, current_user.email)


@router.delete("/delete_item_from_cart/{item_id}", status_code=status.HTTP_200_OK)
def delete_item_from_cart(item_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Delete Item from User Cart
    """
    if admin.is_admin(current_user.email, db):
        raise HTTPException(status_code=401, detail=f"You are not Authorized to view this Page!")
    return users.delete_item_from_cart(item_id, db, current_user.email)


@router.post("/shipping_info", response_model=schemas.ShippingInfo)
def add_shipping_info(request: schemas.ShippingInfo, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Add Shipping Info like Address and other stuff
    """
    if admin.is_admin(current_user.email, db):
        raise HTTPException(status_code=401, detail=f"You are not Authorized to view this Page!")
    return users.add_shipping_info(request, db, current_user.email)


@router.get("/show_shipping_info", response_model=List[schemas.ShippingInfoBase])
def show_shipping_info(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Fetch Shipping Address of Particular User
    """
    if admin.is_admin(current_user.email, db):
        raise HTTPException(status_code=401, detail=f"You are not Authorized to view this Page!")
    return users.show_shipping_info(db, current_user.email)


@router.post("/order_payment")
def order_payment_page(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Get the Payment Link to pay for your Order
    """
    if admin.is_admin(current_user.email, db):
        raise HTTPException(status_code=401, detail=f"You are not Authorized to view this Page!")
    return users.order_payment(db, current_user.email)
