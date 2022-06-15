from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from .. import database, schemas, oauth2
from sqlalchemy.orm import Session
from typing import List, Optional
from ..repository import users

router = APIRouter(
    tags=["User"],
    prefix="/user"
)

get_db = database.get_db


@router.get("/view_products", response_model=List[schemas.Product])
def view_products(db: Session = Depends(get_db)):
    """
    Any User has access to view all the products available in grocery db.
    """
    # if current_user.email == 'admin@admin.in':
    #     raise HTTPException(status_code=401, detail=f"You are not Allowed to view Users Page!")
    return users.view_products(db)


@router.get("/search_products", response_model=List[schemas.Product])
def search_products(item_name: Optional[str] = '', max_price: Optional[float] = 1000, min_price: Optional[float] = 0, db: Session = Depends(get_db)):
    """
    Search Filters to make easy access to required Products.
    """
    name_and_price = users.search_by_name_and_price(item_name, max_price, min_price, db)
    if not name_and_price:
        raise HTTPException(status_code=404, detail=f"No Records Found!!!")
    return name_and_price


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
