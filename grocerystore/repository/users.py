from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import and_, desc, asc
from dotenv import load_dotenv
from .. import models
from ..repository import admin, messages, emailFormat, emailUtil
from ..utils import stripe_gateway, order_placing_query

load_dotenv()

"""
This File does all validations related stuff for users Add | View | Order | Invoice | Payment etc.
All Database query stuff also takes place here.
"""


def view_products(db: Session):
    """
    Return all products available in grocery with all its details
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Data of all Products available in Grocery.
    """
    return db.query(models.Product).order_by(asc(models.Product.id)).all()


def search_by_name(name: str, db: Session):
    """
    Function return products that match the name filter.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    name: str - Matching or Un-matching names of Products
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Data of all Products with similar names in Product title
    """
    return db.query(models.Product).filter(models.Product.title.like(name+'%')).order_by(
        asc(models.Product.id)).all()


def search_by_price(max_price: float, min_price: float, db: Session):
    """
    Function return products that match the price filter.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    max_price: float - Maximum price tag to filter within
    min_price: float - Minimum Price tag to start with
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Data of all Products between the price tag filter
    """
    return db.query(models.Product).filter(models.Product.price > min_price, models.Product.price < max_price).order_by(
        asc(models.Product.id)).all()


def search_by_name_and_price(request, db: Session):
    """
    Common function that returns the products with name/price or name and price filters.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    request: schemas Object - Contains data for Searching Products
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Data of all Products after filtering
    """
    name_and_price = db.query(models.Product).filter(and_(
        and_(models.Product.price > request.min_price, models.Product.price < request.max_price),
        (models.Product.title.like(request.item_name+'%')))).order_by(asc(models.Product.id)).all()
    if not name_and_price:
        raise HTTPException(status_code=404, detail=messages.RECORD_NOT_FOUND)
    return name_and_price


def add_to_cart(request, db: Session, email):
    """
    Function provides validations to add product to cart and increase or decrease items quantity
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    request: Schemas Object - Contains data to find products to add to cart.
    email: str - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Data Confirmation of products added
    """
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
    return messages.json_status_response(200, "Items Successfully Added to Cart")


def my_cart(db: Session, email):
    """
    Functions returns products selected by user.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch All data available in Users-Cart
    """
    if admin.is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    user_id = db.query(models.User.id).filter(models.User.email == email).first()
    my_products = db.query(models.MyCart).filter(models.MyCart.user_id == user_id[0]).all()

    if not my_products:
        raise HTTPException(status_code=404, detail=messages.RECORD_NOT_FOUND)
    return my_products


def add_shipping_info(request, db: Session, email):
    """
    Functions add shipping info/ address info of user to shipping table.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    request: Schemas Object - Contains Shipping Info to be added
    email: str - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Status of Address added
    """
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
    return messages.json_status_response(200, "New Shipping Address Added Successfully.")


def show_shipping_info(db, email):
    """
    Let user view their shipment info (as there are multiple).
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch All data/addresses of User
    """
    if admin.is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    shipping_address = db.query(models.ShippingInfo).filter(and_(models.User.email == email, models.User.id == models.ShippingInfo.user_id)).all()

    if not shipping_address:
        raise HTTPException(status_code=404, detail=messages.RECORD_NOT_FOUND)
    return shipping_address


def delete_item_from_cart(item_id: int, db: Session, email):
    """
    Function helps user to remove items from cart before payout.
    Parameters
    ----------------------------------------------------------
    item_id: int - Product item-ID
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Status of Product removed from cart
    """
    if admin.is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    user_id = db.query(models.User.id).filter(models.User.email == email).first()
    delete_item = db.query(models.MyCart).filter(and_(models.MyCart.user_id == user_id[0]), models.MyCart.product_id == item_id).first()
    if not delete_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.RECORD_NOT_FOUND)

    db.delete(delete_item)
    db.commit()
    return messages.json_status_response(200, "Item Deleted Successfully!")


def order_payment(request, db, email, background_tasks):
    """
    Payment gateway for pay for products owned.
    Parameters
    ----------------------------------------------------------
    request: Schemas Object - Contains data about discount coupon
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In User Session
    background_tasks: BackgroundTasks - Complete Task in Background
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch status of Email-Confirmation of order placed
    """

    if admin.is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    user_id = db.query(models.User.id).filter(models.User.email == email).first()

    """Check User has Items in their Cart before Proceed."""
    check_cart_existence = order_placing_query.check_cart(db, user_id)

    """Check User has added their Shipping Information."""
    shipping_info = order_placing_query.shipment_info(request, db, user_id)

    """Fetch the Coupon Code and verify"""
    coupon_discount, coupon_using = order_placing_query.coupon_code_validation(db, user_id, request)

    """Fetch the Total Amount Payable By User"""
    total_amount = order_placing_query.order_amount(request, db, user_id, coupon_discount)

    """
    Generate Invoice for User Orders
    Using Stripe Payment Gateway
    """
    invoice = stripe_gateway.strip_payment_gateway(total_amount, email)

    """Check Quantity of Product in Grocery and decrease if Order is purchased By User"""
    product_details = db.query(models.Product).filter(
        and_(models.MyCart.user_id == user_id[0], models.Product.id == models.MyCart.product_id)).all()
    for i, j in zip(product_details, check_cart_existence):
        i.quantity = (getattr(i, "quantity") - getattr(j, "product_quantity"))

    for prod_name in check_cart_existence:
        new_order = models.OrderDetails(
            user_id=user_id[0],
            shipping_id=getattr(shipping_info, "id"),
            description=invoice['id'],
            payment_id=invoice['payment_intent'],
            product_name=getattr(prod_name, "product_name"),
            total_amount=getattr(prod_name, "total"),
            coupon_used=coupon_using
        )
        db.add(new_order)

    db.query(models.MyCart).filter(models.MyCart.user_id == user_id[0]).delete()
    db.commit()

    """Formatting Email"""
    subject, recipient, message = emailFormat.invoiceFormat(email, invoice, shipping_info,
                                                            check_cart_existence, coupon_discount,
                                                            total_amount)

    """Sending Email to User"""
    background_tasks.add_task(emailUtil.send_email, subject, recipient, message)
    return messages.json_status_response(200, "Please Find your Invoice on your email.")


def webhook_received(db, payment_intent, payment_status):
    update_payment_status = db.query(models.OrderDetails).filter(models.OrderDetails.payment_id == payment_intent).all()
    for i in update_payment_status:
        i.payment_status = payment_status

    db.commit()
    return {"Status": "Status Received"}


def order_history(db, email):
    """
    Users all Order History Till Date and its Info
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch All data of Previous Orders
    """
    if admin.is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    user_id = db.query(models.User.id).filter(models.User.email == email).first()
    history = db.query(models.OrderDetails).filter(models.OrderDetails.user_id == user_id[0]).order_by(desc(models.OrderDetails.id)).all()
    if not history:
        raise HTTPException(status_code=404, detail=messages.RECORD_NOT_FOUND)
    return history


def return_item(item_id: int, db, email):
    """
    Cancel Order and RefundOrder Amount to Wallet Section.
    Parameters
    ----------------------------------------------------------
    item_id: int - Order ID
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Status of order cancellation
    """
    if admin.is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    user_id = db.query(models.User.id).filter(models.User.email == email).first()
    my_order = db.query(models.OrderDetails).filter(and_(models.OrderDetails.id == item_id,
                                                         models.OrderDetails.user_id == user_id[0],
                                                         models.OrderDetails.payment_status != "refunded")).first()
    if not my_order:
        raise HTTPException(status_code=404, detail=messages.RECORD_NOT_FOUND)
    my_order.payment_status = "refunded"
    my_order.order_status = "returned"

    refund_amount = getattr(my_order, "total_amount")
    refund_amount -= (refund_amount*0.1)
    my_wallet = db.query(models.MyWallet).filter(models.MyWallet.user_id == user_id[0]).first()
    my_wallet.acc_balance = (getattr(my_wallet, "acc_balance") + refund_amount)

    db.commit()

    return messages.json_status_response(200, "Amount will be Refunded to your Wallet. 10% Cancellation Charges are applied.")


def cancel_order(order_id: str, db, email):
    """
    Cancel Order and RefundOrder Amount to Wallet Section.
    Parameters
    ----------------------------------------------------------
    order_id: str - Order ID
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Status of order cancellation
    """
    if admin.is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    user_id = db.query(models.User.id).filter(models.User.email == email).first()
    my_order = db.query(models.OrderDetails).filter(and_(models.OrderDetails.description == order_id,
                                                         models.OrderDetails.user_id == user_id[0],
                                                         models.OrderDetails.payment_status != "refunded")).all()
    if not my_order:
        raise HTTPException(status_code=404, detail=messages.RECORD_NOT_FOUND)
    refund_amount = 0
    for i in my_order:
        refund_amount += getattr(i, "total_amount")
        i.payment_status = "refunded"
        i.order_status = "returned"

    refund_amount -= (refund_amount * 0.1)
    my_wallet = db.query(models.MyWallet).filter(models.MyWallet.user_id == user_id[0]).first()
    my_wallet.acc_balance = (getattr(my_wallet, "acc_balance") + refund_amount)

    db.commit()

    return messages.json_status_response(200, "Amount will be Refunded to your Wallet. 10% Cancellation Charges are applied.")


def track_order_status(request, db, email):
    """
    Cancel Order and RefundOrder Amount to Wallet Section.
    Parameters
    ----------------------------------------------------------
    request: schemas Object - Order ID
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Status of order cancellation
    """
    if admin.is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    check_order_id = db.query(models.OrderDetails).filter(models.OrderDetails.description == request.order_tracking_id).all()

    if not check_order_id:
        raise HTTPException(status_code=404, detail=messages.RECORD_NOT_FOUND)

    return check_order_id


def view_balance(db, email):
    """
    Fetch the Account Balance in Wallet.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    email: str - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Available balance in users wallet
    """
    if admin.is_admin(email, db):
        raise HTTPException(status_code=401, detail=messages.NOT_AUTHORIZE_401)

    user_id = db.query(models.User.id).filter(models.User.email == email).first()
    balance = db.query(models.MyWallet).filter(models.MyWallet.user_id == user_id[0]).first()

    return balance


def show_discount_coupon(db: Session):
    """
    Return all discount coupon details .
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch All Data of applicable coupons
    """
    return db.query(models.DiscountCoupon).all()
