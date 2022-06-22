from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models
from sqlalchemy import and_, func
import razorpay


def view_products(db: Session):
    """Return all products available in grocery with all its details"""
    return db.query(models.Product).all()


def search_by_name(name: str, db: Session):
    """Function return products that match the name filter."""
    return db.query(models.Product).filter(models.Product.title.like(name+'%')).all()


def search_by_price(max_price: float, min_price: float, db: Session):
    """Function return products that match the price filter."""
    return db.query(models.Product).filter(models.Product.price > min_price, models.Product.price < max_price).all()


def search_by_name_and_price(request, db: Session):
    """Common function that returns the products with name/price or name and price filters."""
    return db.query(models.Product).filter(and_(and_(models.Product.price > request.min_price, models.Product.price < request.max_price), (models.Product.title.like(request.item_name+'%')))).all()


def add_to_cart(request, db: Session, email):
    """Function provides validations to add product to cart and increase or decrease items quantity"""
    user_id = db.query(models.User.id).filter(models.User.email == email).first()
    product_id = db.query(models.Product).filter(models.Product.id == request.item_id).first()

    """Check Product Exists or Not"""
    if not product_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with {request.item_id} Not Exists.")

    stock_id = getattr(product_id, "id")
    stock_quantity = getattr(product_id, "quantity")
    stock_title = getattr(product_id, "title")
    stock_price = getattr(product_id, "price")

    """Check Product Availability."""
    if request.item_quantity > getattr(product_id, "quantity"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Stock UnAvailable! {stock_quantity} Stocks left.")

    """Check Product Already Exists in Cart or not"""
    my_products = db.query(models.MyCart).filter(models.MyCart.user_id == user_id[0]).all()
    for i in my_products:
        total_product_quantity = (getattr(i, "product_quantity") + request.item_quantity)
        if request.item_id == getattr(i, "product_id"):
            if total_product_quantity > getattr(product_id, "quantity"):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Out of Stock")
            else:
                i.product_quantity = (getattr(i, "product_quantity") + request.item_quantity)
                i.total = (getattr(i, "total") + (stock_price*request.item_quantity))
                db.commit()
                return {"Status": "Item Updated Successfully..."}

    """Add Product Details to MyCart."""
    cart_item = models.MyCart(
        user_id=user_id[0],
        product_id=stock_id,
        product_name=stock_title,
        product_quantity=request.item_quantity,
        product_price=stock_price,
        total=stock_price*request.item_quantity
    )
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return {"Status": "Item Added to your Cart"}


def my_cart(db: Session, email):
    """Functions returns products selected by user."""
    user_id = db.query(models.User.id).filter(models.User.email == email).first()
    my_products = db.query(models.MyCart).filter(models.MyCart.user_id == user_id[0]).all()
    return my_products


def add_shipping_info(request, db: Session, email):
    """Functions add shipping info/ address info of user to shipping table."""
    user_id = db.query(models.User.id).filter(models.User.email == email).first()
    new_address = models.ShippingInfo(
        name=request.name,
        phone_no=request.phone_no,
        address=request.address,
        city=request.city,
        state=request.state,
        user_id=user_id[0]
    )
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address


def show_shipping_info(db, email):
    """Let user view their shipment info (as there are multiple)."""
    return db.query(models.ShippingInfo).filter(and_(models.User.email == email, models.User.id == models.ShippingInfo.user_id)).all()


def delete_item_from_cart(item_id: int, db: Session, email):
    """Function helps user to remove items from cart before payout."""
    user_id = db.query(models.User.id).filter(models.User.email == email).first()
    delete_item = db.query(models.MyCart).filter(and_(models.MyCart.user_id == user_id[0]), models.MyCart.product_id == item_id).first()
    if not delete_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Does Not Exists!!!")
    item_to_be_deleted = getattr(delete_item, "product_name")
    db.delete(delete_item)
    db.commit()
    return {f"Product {item_to_be_deleted}": "Deleted Successfully"}


def order_payment(db, email):
    """Payment gateway for pay for products owned."""
    user_id = db.query(models.User.id).filter(models.User.email == email).first()

    """Check User has Items in their Cart before Proceed."""
    check_cart_existence = db.query(models.MyCart).filter(models.MyCart.user_id == user_id[0]).all()
    if not check_cart_existence:
        raise HTTPException(status_code=404, detail="No Items found in your Cart. Please add items to your Cart.")

    """Check User has added their Shipping Information."""
    shipping_info = db.query(models.ShippingInfo).filter(models.ShippingInfo.user_id == user_id[0]).first()
    if not shipping_info:
        raise HTTPException(status_code=404, detail="Please Provide Your Shipping Info. And proceed with Payment")

    """Fetch the Total Amount Payable By User"""
    total_amount = db.query(func.sum(models.MyCart.total)).filter(models.MyCart.user_id == user_id[0]).all()

    """Check Quantity of Product in Grocery and decrease if Order is purchased By User"""
    product_details = db.query(models.Product).filter(and_(models.MyCart.user_id == user_id[0], models.Product.id == models.MyCart.product_id)).all()
    for i, j in zip(product_details, check_cart_existence):
        i.quantity = (getattr(i, "quantity") - getattr(j, "product_quantity"))

    """Generate Invoice for User Orders"""
    client = razorpay.Client(auth=("rzp_test_zy1IBpjZKAWeCs", "C4uGQ8GQQDQueR5IRownJKVM"))
    invoice = client.order.create({'amount': total_amount[0][0]*100, 'currency': 'INR', 'payment_capture': '1', 'notes': [
            'Thank You! Please Visit Again...'
    ]})

    new_order = models.OrderDetails(
        user_id=user_id[0],
        shipping_id=getattr(shipping_info, "id"),
        description=invoice['id'],
        total_amount=total_amount[0][0],
        payment_status="completed"
    )

    db.add(new_order)
    db.query(models.MyCart).filter(models.MyCart.user_id == user_id[0]).delete()

    db.commit()
    db.refresh(new_order)

    return invoice
