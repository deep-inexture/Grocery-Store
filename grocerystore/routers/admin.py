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


@router.get("/get_items", response_model=List[schemas.Product])
def all_products(db: Session= Depends(get_db), current_user: schemas.User= Depends(oauth2.get_current_user)):
    """FETCH ALL PRODUCTS AVAILABLE IN GROCERY"""
    return admin.all_products(db)


@router.post("/create_items", status_code=status.HTTP_201_CREATED)
def add_product(request: List[schemas.ProductBase], db: Session= Depends(get_db), current_user: schemas.User= Depends(oauth2.get_current_user)):
    # file_location = f"{ROOT_DIR}/product_image/{product_image.filename}"
    # suffix = Path(product_image.filename).suffix
    # if suffix in ['.png', '.jpg', '.jpeg']:
    #     with open(file_location, "wb+") as file_object:
    #         shutil.copyfileobj(product_image.file, file_object)
    #     print(product_image.file)

    admin.add_product(request, db)
    return {'DB Status': 'Item Added Successfully'}


@router.put("/update_item/{item_id}", status_code=status.HTTP_200_OK)
def update_product(item_id: int, item: schemas.ProductBase, db: Session= Depends(get_db), current_user: schemas.User= Depends(oauth2.get_current_user)):
    check_item_id = db.query(models.Product).filter(models.Product.id == item_id).first()
    if not check_item_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with ID: ({item_id}) NOT FOUND!!!")

    items_found = admin.fetch_data(item_id, db)
    image_file = getattr(items_found, 'image_file')
    title = getattr(items_found, 'title')
    description = getattr(items_found, 'description')
    price = getattr(items_found, 'price')
    quantity = getattr(items_found, 'quantity')

    if image_file == item.image_file and title == item.title and description == item.description and price == item.price and quantity == item.quantity:
        raise HTTPException(status_code=302, detail=f"No Change Detected!")

    check_item_id.image_file = item.image_file
    check_item_id.title = item.title
    check_item_id.description = item.description
    check_item_id.price = item.price
    check_item_id.quantity = item.quantity

    db.commit()
    return {f"Product Image =       {image_file}": f"changed to {check_item_id.image_file}",
            f"Product Title =       {title}": f"changed to {check_item_id.title}",
            f"Product Description = {description}": f"changed to {check_item_id.description}",
            f"Product Price =       {price}": f"changed to {check_item_id.price}",
            f"Product Quantity =    {quantity}": f"changed to {check_item_id.quantity}"}


@router.delete("/delete_item/{item_id}", status_code=status.HTTP_200_OK)
def delete_product(item_id: int, db: Session= Depends(get_db), current_user: schemas.User= Depends(oauth2.get_current_user)):
    delete_item = db.query(models.Product).filter(models.Product.id == item_id).first()
    if delete_item is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Item Does Not Exists!!!")
    items_found = admin.fetch_data(item_id, db)
    title = getattr(items_found, 'title')
    db.delete(delete_item)
    db.commit()
    return {f"Product {title}": "Deleted Successfully"}