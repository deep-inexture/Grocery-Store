import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import and_, func, desc, asc
import razorpay
from dotenv import load_dotenv
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import models
from repository import admin, messages, emailFormat, emailUtil

load_dotenv()


def view_products(db: Session):
    """Return all products available in grocery with all its details"""
    return db.query(models.Product).order_by(asc(models.Product.id)).all()


def search_by_name(name: str, db: Session):
    """Function return products that match the name filter."""
    return db.query(models.Product).filter(models.Product.title.like(name+'%')).all()


def search_by_price(max_price: float, min_price: float, db: Session):
    """Function return products that match the price filter."""
    return db.query(models.Product).filter(models.Product.price > min_price, models.Product.price < max_price).all()


def search_by_name_and_price(request, db: Session):
    """Common function that returns the products with name/price or name and price filters."""
    name_and_price = db.query(models.Product).filter(and_(and_(models.Product.price > request.min_price, models.Product.price < request.max_price), (models.Product.title.like(request.item_name+'%')))).all()
    if not name_and_price:
        raise HTTPException(status_code=404, detail=messages.RECORD_NOT_FOUND)
    return name_and_price


def add_to_cart(request, db: Session, email):
    """Function provides validations to add product to cart and increase or decrease items quantity"""
    if admin.is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    user_id = db.query(models.User.id).filter(models.User.email == email).first()
    product_id = db.query(models.Product).filter(models.Product.id == request.item_id).first()

    """Check Product Exists or Not"""
    if not product_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.Product_Not_Found_404(request.item_id))

    stock_id = getattr(product_id, "id")
    stock_quantity = getattr(product_id, "quantity")
    stock_title = getattr(product_id, "title")
    stock_price = getattr(product_id, "price")

    """Check Product Availability."""
    if request.item_quantity > getattr(product_id, "quantity"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.Stock_Unavailable_404(stock_quantity))

    """Check Product Already Exists in Cart or not"""
    my_products = db.query(models.MyCart).filter(models.MyCart.user_id == user_id[0]).all()
    for i in my_products:
        total_product_quantity = (getattr(i, "product_quantity") + request.item_quantity)
        if request.item_id == getattr(i, "product_id"):
            if total_product_quantity > getattr(product_id, "quantity"):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.OUT_OF_STOCK)
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
    if admin.is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    user_id = db.query(models.User.id).filter(models.User.email == email).first()
    my_products = db.query(models.MyCart).filter(models.MyCart.user_id == user_id[0]).all()

    if not my_products:
        raise HTTPException(status_code=404, detail=messages.RECORD_NOT_FOUND)
    return my_products


def add_shipping_info(request, db: Session, email):
    """Functions add shipping info/ address info of user to shipping table."""
    if admin.is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    if len(request.phone_no) != 10:
        raise HTTPException(status_code=401, detail=messages.INVALID_PHONE_401)

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
    if admin.is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    shipping_address = db.query(models.ShippingInfo).filter(and_(models.User.email == email, models.User.id == models.ShippingInfo.user_id)).all()

    if not shipping_address:
        raise HTTPException(status_code=404, detail=messages.RECORD_NOT_FOUND)
    return shipping_address


def delete_item_from_cart(item_id: int, db: Session, email):
    """Function helps user to remove items from cart before payout."""
    if admin.is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    user_id = db.query(models.User.id).filter(models.User.email == email).first()
    delete_item = db.query(models.MyCart).filter(and_(models.MyCart.user_id == user_id[0]), models.MyCart.product_id == item_id).first()
    if not delete_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.RECORD_NOT_FOUND)
    item_to_be_deleted = getattr(delete_item, "product_name")
    db.delete(delete_item)
    db.commit()
    return {f"Product {item_to_be_deleted}": "Deleted Successfully"}


def order_payment(request, db, email):
    """Payment gateway for pay for products owned."""
    if admin.is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    user_id = db.query(models.User.id).filter(models.User.email == email).first()

    """Check User has Items in their Cart before Proceed."""
    check_cart_existence = db.query(models.MyCart).filter(models.MyCart.user_id == user_id[0]).all()
    if not check_cart_existence:
        raise HTTPException(status_code=404, detail=messages.CART_EMPTY_404)

    """Check User has added their Shipping Information."""
    shipping_info = db.query(models.ShippingInfo).filter(models.ShippingInfo.user_id == user_id[0]).first()
    if not shipping_info:
        raise HTTPException(status_code=404, detail=messages.SHIPPING_UNAVAILABLE_404)

    """Fetch the Coupon Code and verify"""
    coupon_code = db.query(models.DiscountCoupon).filter(models.DiscountCoupon.coupon_code == request.coupon_code).first()
    if str(getattr(coupon_code, "valid_till")) < datetime.date.today().strftime("%Y-%m-%d"):
        raise HTTPException(status_code=401, detail=messages.COUPON_EXPIRED_404)

    if request.coupon_code == "":
        coupon_discount = 0
    elif not coupon_code:
        raise HTTPException(status_code=404, detail=messages.RECORD_NOT_FOUND)
    else:
        coupon_discount = getattr(coupon_code, "discount_percentage")
        coupon_code.times_used = getattr(coupon_code, "times_used") + 1

    """Fetch the Total Amount Payable By User"""
    total_amount = db.query(func.sum(models.MyCart.total)).filter(models.MyCart.user_id == user_id[0]).all()
    total_amount = (total_amount[0][0] - ((total_amount[0][0]*coupon_discount)/100))

    """Check Quantity of Product in Grocery and decrease if Order is purchased By User"""
    product_details = db.query(models.Product).filter(and_(models.MyCart.user_id == user_id[0], models.Product.id == models.MyCart.product_id)).all()
    for i, j in zip(product_details, check_cart_existence):
        i.quantity = (getattr(i, "quantity") - getattr(j, "product_quantity"))

    """Generate Invoice for User Orders"""
    RZP_KEY_ID = os.environ.get('RZP_KEY_ID')
    RZP_SECRET_KEY = os.environ.get('RZP_SECRET_KEY')
    client = razorpay.Client(auth=(RZP_KEY_ID, RZP_SECRET_KEY))
    invoice = client.order.create({'amount': total_amount*100, 'currency': 'INR', 'payment_capture': '1',
                                   'notes': ['Thank You! Please Visit Again...', 'https://rzp.io/i/njYysZq'],
                                   })

    new_order = models.OrderDetails(
        user_id=user_id[0],
        shipping_id=getattr(shipping_info, "id"),
        description=invoice['id'],
        total_amount=total_amount,
        payment_status="completed"
    )

    db.add(new_order)
    db.query(models.MyCart).filter(models.MyCart.user_id == user_id[0]).delete()

    db.commit()
    db.refresh(new_order)

    """Formatting Email"""
    subject, recipient, message = emailFormat.invoiceFormat(email, invoice, shipping_info,
                                                            len(check_cart_existence),
                                                            coupon_discount)

    """Sending Email to User"""
    emailUtil.send_email(subject, recipient, message)

    return {"message": "Please Find your Invoice on your email."}


def order_history(db, email):
    """Users all Order History Till Date and its Info"""
    if admin.is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    user_id = db.query(models.User.id).filter(models.User.email == email).first()
    history = db.query(models.OrderDetails).filter(models.OrderDetails.user_id == user_id[0]).order_by(desc(models.OrderDetails.id)).all()
    if not history:
        raise HTTPException(status_code=404, detail=messages.RECORD_NOT_FOUND)
    return history


def cancel_order(item_id: int, db, email):
    """Cancel Order and RefundOrder Amount to Wallet Section."""
    if admin.is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    user_id = db.query(models.User.id).filter(models.User.email == email).first()
    my_order = db.query(models.OrderDetails).filter(and_(models.OrderDetails.id == item_id,
                                                         models.OrderDetails.user_id == user_id[0])).first()
    if not my_order:
        raise HTTPException(status_code=404, detail=messages.RECORD_NOT_FOUND)
    my_order.payment_status = "refunded"

    refund_amount = getattr(my_order, "total_amount")
    refund_amount -= (refund_amount*0.1)
    my_wallet = db.query(models.MyWallet).filter(models.MyWallet.user_id == user_id[0]).first()
    my_wallet.acc_balance = (getattr(my_wallet, "acc_balance") + refund_amount)

    db.commit()

    return {
        "Order-ID": f"Order with ID: {getattr(my_order, 'description')} has been Cancelled.",
        "Amount": f"Amount of Rs.{getattr(my_wallet, 'acc_balance')} has been Refunded",
        "message": f"Amount will be Refunded to your Wallet. 10% Cancellation Charges are applied."
    }


def view_balance(db, email):
    """Fetch the Account Balance in Wallet."""
    if admin.is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    user_id = db.query(models.User.id).filter(models.User.email == email).first()
    balance = db.query(models.MyWallet).filter(models.MyWallet.user_id == user_id[0]).first()

    return balance


def show_discount_coupon(db: Session):
    """Return all discount coupon details ."""
    return db.query(models.DiscountCoupon).all()