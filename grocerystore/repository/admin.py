from sqlalchemy.orm import Session
from .. import models, schemas
from typing import List


def all_products(db: Session):
    items = db.query(models.Product).all()
    return items


def add_product(request: List[schemas.Product], db: Session):
    for items in request:
        new_item = models.Product(
            image_file=items.image_file,
            title=items.title,
            description=items.description,
            price=items.price,
            quantity=items.quantity
        )
        db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {'status': 'Done'}