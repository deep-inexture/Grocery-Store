from fastapi import APIRouter, Depends, status
from .. import database, schemas, oauth2
from sqlalchemy.orm import Session
from typing import List
from ..repository import users
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


@router.post("/search_products", response_model=List[schemas.Product])
def search_products(request: schemas.SearchProduct, db: Session = Depends(get_db)):
    """
    Search Filters to make easy access to required Products.
    """
    return users.search_by_name_and_price(request, db)


@router.post("/add_to_cart", status_code=status.HTTP_200_OK)
def add_to_cart(request: schemas.AddToCart, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Add your favorite Item to your Cart by entering item id from view products/ search products.
    """
    return users.add_to_cart(request, db, current_user.email)


@router.get("/view_my_cart", response_model=List[schemas.MyCartBase])
def my_cart(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    User can view their Cart and their Products Added to cart
    """
    return users.my_cart(db, current_user.email)


@router.delete("/delete_item_from_cart/{item_id}", status_code=status.HTTP_200_OK)
def delete_item_from_cart(item_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Delete Item from User Cart
    """
    return users.delete_item_from_cart(item_id, db, current_user.email)


@router.post("/shipping_info", response_model=schemas.ShippingInfo)
def add_shipping_info(request: schemas.ShippingInfo, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Add Shipping Info like Address and other stuff
    """
    return users.add_shipping_info(request, db, current_user.email)


@router.get("/show_shipping_info", response_model=List[schemas.ShippingInfoBase])
def show_shipping_info(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Fetch Shipping Address of Particular User
    """
    return users.show_shipping_info(db, current_user.email)


@router.post("/order_payment")
def order_payment_page(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Get the Payment Link to pay for your Order
    """
    return users.order_payment(db, current_user.email)


@router.get("/order_history")
def order_history(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Show User their Last Order History.
    """
    return users.order_history(db, current_user.email)


@router.delete('/cancel_order/{item_id}')
def cancel_order(item_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Fetch the item_id from User to cancel the order and refund amount to Wallet.
    """
    return users.cancel_order(item_id, db, current_user.email)


@router.get('/view_balance', response_model=schemas.WalletBalance)
def view_balance(db: Session= Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Fetch the User Wallet Balance.
    """
    return users.view_balance(db, current_user.email)


add_pagination(router)
