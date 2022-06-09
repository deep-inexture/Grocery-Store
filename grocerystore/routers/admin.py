import shutil

from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from .. import database, schemas, models, hashing, oauth2
from ..hashing import Hash
from typing import List
from pathlib import Path
import os
from ..repository import admin
from tempfile import NamedTemporaryFile

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

router = APIRouter(
    tags=["Admin"],
    prefix="/admin"
)
get_db = database.get_db


# @router.get('/user/{id}', response_model=schemas.ShowUser)
# def get_user(id: int, db: Session= Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} NOT FOUND!")
#     return user


@router.get("/", response_model=List[schemas.Product])
def all_products(db: Session= Depends(get_db), current_user: schemas.User= Depends(oauth2.get_current_user)):
    """FETCH ALL PRODUCTS AVAILABLE IN GROCERY"""
    return admin.all_products(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_product(request: List[schemas.Product], db: Session= Depends(get_db), current_user: schemas.User= Depends(oauth2.get_current_user)):
    # file_location = f"{ROOT_DIR}/product_image/{product_image.filename}"
    # suffix = Path(product_image.filename).suffix
    # if suffix in ['.png', '.jpg', '.jpeg']:
    #     with open(file_location, "wb+") as file_object:
    #         shutil.copyfileobj(product_image.file, file_object)
    #     print(product_image.file)

    admin.add_product(request, db)
    return {'DB Status': 'Item Added Successfully'}
