from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from fastapi_pagination import Page, add_pagination, paginate, LimitOffsetPage
from .. import database, schemas, oauth2
from ..repository import users

"""
Users Routing structure is placed here. Pagination and other Session dependencies are made over
here. 
"""

router = APIRouter(
    tags=["User"],
    prefix="/user",
)

get_db = database.get_db


@router.get("/view_products", response_model=Page[schemas.Product])
@router.get("/view_products/limit-offset", response_model=LimitOffsetPage[schemas.Product])
def view_products(db: Session = Depends(get_db)):
    """
    Any User has access to view all the products available in grocery db.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Data of all Products available in Grocery.
    """
    return paginate(users.view_products(db))


@router.post("/search_products", response_model=List[schemas.Product])
def search_products(request: schemas.SearchProduct, db: Session = Depends(get_db)):
    """
    Search Filters to make easy access to required Products.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    request: schemas Object - Contains data for Searching Products
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Data of all Products after filter
    """
    return users.search_by_name_and_price(request, db)


@router.post("/add_to_cart", status_code=status.HTTP_200_OK)
def add_to_cart(request: schemas.AddToCart, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Add your favorite Item to your Cart by entering item id from view products/ search products.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    request: Schemas Object - Contains data to find products to add to cart.
    current_user: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Data Confirmation of products added
    """
    return users.add_to_cart(request, db, current_user.email)


@router.get("/view_my_cart", response_model=List[schemas.MyCartBase])
def my_cart(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    User can view their Cart and their Products Added to cart
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    current_user: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch All data available in Users-Cart
    """
    return users.my_cart(db, current_user.email)


@router.delete("/delete_item_from_cart/{item_id}", status_code=status.HTTP_200_OK)
def delete_item_from_cart(item_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Delete Item from User Cart
    Parameters
    ----------------------------------------------------------
    item_id: int - Product item-ID
    db: Database Object - Fetching Schemas Content
    current_user: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Status of Product removed from cart
    """
    return users.delete_item_from_cart(item_id, db, current_user.email)


@router.post("/shipping_info", response_model=schemas.ShippingInfo)
def add_shipping_info(request: schemas.ShippingInfo, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Add Shipping Info like Address and other stuff
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    request: Schemas Object - Contains Shipping Info to be added
    current_user: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Status of Address added
    """
    return users.add_shipping_info(request, db, current_user.email)


@router.get("/show_shipping_info", response_model=List[schemas.ShippingInfoBase])
def show_shipping_info(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Fetch Shipping Address of Particular User
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    current_user: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch All data/addresses of User
    """
    return users.show_shipping_info(db, current_user.email)


@router.post("/order_payment")
def order_payment_page(request: schemas.CheckDiscountCoupon, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Get the Payment Link to pay for your Order
    Parameters
    ----------------------------------------------------------
    request: Schemas Object - Contains data about discount coupon
    db: Database Object - Fetching Schemas Content
    current_user: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch status of Email-Confirmation of order placed
    """
    return users.order_payment(request, db, current_user.email)


@router.get("/order_history")
def order_history(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Show User their Last Order History.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    current_user: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch All data of Previous Orders
    """
    return users.order_history(db, current_user.email)


@router.delete('/cancel_order/{item_id}')
def cancel_order(item_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Fetch the item_id from User to cancel the order and refund amount to Wallet.
    Parameters
    ----------------------------------------------------------
    item_id: int - Order ID
    db: Database Object - Fetching Schemas Content
    current_user: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Status of order cancellation
    """
    return users.cancel_order(item_id, db, current_user.email)


@router.get('/view_balance', response_model=schemas.WalletBalance)
def view_balance(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Fetch the User Wallet Balance.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    current_user: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Available balance in users wallet
    """
    return users.view_balance(db, current_user.email)


@router.get('/show_discount_coupon', response_model=List[schemas.ShowDiscountCoupon])
def show_discount_coupon(db: Session = Depends(get_db)):
    """
    Get All the Discount Coupons Visible.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch All Data of applicable coupons
    """
    return users.show_discount_coupon(db)


add_pagination(router)
