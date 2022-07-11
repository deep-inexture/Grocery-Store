import datetime
from sqlalchemy import distinct, func, and_
from fastapi import HTTPException
from ..repository import messages
from .. import models


def check_cart(db, user_id):
    """Check User has Items in their Cart before Proceed."""
    check_cart_existence = db.query(models.MyCart).filter(models.MyCart.user_id == user_id[0]).all()
    if not check_cart_existence:
        raise HTTPException(status_code=404, detail=messages.CART_EMPTY_404)
    return check_cart_existence


def shipment_info(request, db, user_id):
    """Check User has added their Shipping Information."""
    shipping_info = db.query(models.ShippingInfo).filter(and_(models.ShippingInfo.user_id == user_id[0], models.ShippingInfo.id == request.shipping_id)).first()
    if not shipping_info:
        raise HTTPException(status_code=404, detail=messages.SHIPPING_UNAVAILABLE_404)
    return shipping_info


def coupon_code_validation(db, user_id, request):
    """Fetch the Coupon Code and verify"""
    coupon_code = db.query(models.DiscountCoupon).filter(
        models.DiscountCoupon.coupon_code == request.coupon_code).first()
    if request.coupon_code == "":
        coupon_discount = 0
        coupon_using = 0
    elif not coupon_code:
        raise HTTPException(status_code=404, detail=messages.INVALID_COUPON_CODE)
    else:
        if str(getattr(coupon_code, "valid_till")) < datetime.date.today().strftime("%Y-%m-%d"):
            raise HTTPException(status_code=401, detail=messages.COUPON_EXPIRED_404)
        coupon_discount = getattr(coupon_code, "discount_percentage")
        coupon_using = getattr(coupon_code, "id")
        coupon_code.times_used = getattr(coupon_code, "times_used") + 1

        """Check Coupon used once or not"""
        order_details = db.query(distinct(models.OrderDetails.coupon_used)).filter(
            models.OrderDetails.user_id == user_id[0])
        for i in order_details:
            if coupon_using == i[0]:
                raise HTTPException(status_code=401, detail=messages.USED_COUPON_401)

    return coupon_discount, coupon_using


def order_amount(request, db, user_id, coupon_discount):
    """Fetch the Total Amount Payable By User"""
    total_amount = db.query(func.sum(models.MyCart.total)).filter(models.MyCart.user_id == user_id[0]).all()

    if total_amount[0][0] < 100:
        raise HTTPException(status_code=401, detail=messages.LOW_ORDER_AMOUNT.format(100 - total_amount[0][0]))

    product_type = db.query(models.Product.product_type).filter(
        and_(models.MyCart.product_id == models.Product.id, models.MyCart.user_id == user_id[0])).all()

    for i in product_type:
        if request.coupon_code == "":
            coupon_found = 1
            break
        elif request.coupon_code == i[0]:
            coupon_found = 1
            item_total_amount = db.query(func.sum(models.MyCart.total)).filter(
                and_(models.MyCart.product_id == models.Product.id, models.MyCart.user_id == user_id[0],
                     models.Product.product_type == request.coupon_code))

            total_amount = (total_amount[0][0] - ((item_total_amount[0][0] * coupon_discount) / 100))
            return total_amount
        else:
            coupon_found = 0

    if coupon_found == 0:
        raise HTTPException(status_code=404, detail=messages.INVALID_COUPON_404)

    total_amount = (total_amount[0][0] - ((total_amount[0][0] * coupon_discount) / 100))
    return total_amount
