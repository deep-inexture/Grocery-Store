from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from .. import database, schemas, oauth2
from sqlalchemy.orm import Session
from typing import List
from ..repository import users

router = APIRouter(
    tags=["User"],
    prefix="/user"
)

get_db = database.get_db


@router.get("/view_products", response_model=List[schemas.Product])
def view_products(db: Session= Depends(get_db)):
    """
    Any User has access to view all the products available in grocery db.
    """
    return users.view_products(db)


@router.get("/search_products", response_model=List[schemas.Product])
def search_products(item_name: str, max_price: float, min_price: float, db: Session= Depends(get_db), current_user: schemas.User= Depends(oauth2.get_current_user)):
    """
    Search Filters to make easy access to required Products.
    """
    name = users.search_by_name(item_name, db)
    return name
