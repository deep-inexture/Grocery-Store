import shutil
from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from .. import database, schemas, models, oauth2
from typing import List
from pathlib import Path
import os
from ..repository import admin
from tempfile import NamedTemporaryFile
from functools import wraps

# This File Contains all Admin Related Routes such as ADD | UPDATE | DELETE Products and many more.
# All validations and query gets fired in other file with same name in repository directory.

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

router = APIRouter(
    tags=["Admin"],
    prefix="/admin"
)
get_db = database.get_db


# def is_admin(email):
#     if email == 'admin@admin.in':
#         return True

# @router.get('/user/{id}', response_model=schemas.ShowUser)
# def get_user(id: int, db: Session= Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} NOT FOUND!")
#     return user


@router.get("/get_items", response_model=List[schemas.Product])
def all_products(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    FETCH ALL PRODUCTS AVAILABLE IN GROCERY
    """
    if not admin.is_admin(current_user.email, db):
        raise HTTPException(status_code=401, detail=f"You are not Authorized to view this Page!")
    return admin.all_products(db)


@router.post("/create_items", status_code=status.HTTP_201_CREATED)
def add_product(request: List[schemas.ProductBase], db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    ADD PRODUCTS TO SHOW IN GROCERY
    """
    if not admin.is_admin(current_user.email, db):
        raise HTTPException(status_code=401, detail=f"You are not Authorized to view this Page!")
    # file_location = f"{ROOT_DIR}/product_image/{product_image.filename}"
    # suffix = Path(product_image.filename).suffix
    # if suffix in ['.png', '.jpg', '.jpeg']:
    #     with open(file_location, "wb+") as file_object:
    #         shutil.copyfileobj(product_image.file, file_object)
    #     print(product_image.file)

    admin.add_product(request, db)
    return {'DB Status': 'Item Added Successfully'}


@router.put("/update_item/{item_id}", status_code=status.HTTP_200_OK)
def update_product(item_id: int, item: schemas.ProductBase, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    UPDATE PRODUCTS FOR GROCERY
    """
    if not admin.is_admin(current_user.email, db):
        raise HTTPException(status_code=401, detail=f"You are not Authorized to view this Page!")
    return admin.update_product(item_id, db, item)


@router.delete("/delete_item/{item_id}", status_code=status.HTTP_200_OK)
def delete_product(item_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    DELETE ITEMS NOT IN GROCERY
    """
    if not admin.is_admin(current_user.email, db):
        raise HTTPException(status_code=401, detail=f"You are not Authorized to view this Page!")
    return admin.delete_product(item_id, db)
