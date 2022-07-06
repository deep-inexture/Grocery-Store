"""
Collection of all Error and Success Messages for overall project.
"""


NO_CHANGES_302 = "No Change Detected!"
NOT_AUTHORIZE_401 = "You are not Authorized to view this Page!"
INVALID_EMAIL_401 = "Invalid Email-ID Format!!!"
INVALID_DATE_401 = "Invalid Date! Please Enter Correct Dates."
INVALID_PHONE_401 = "Invalid Phone Number Format! Phone Number Should Contain Exact 10 Numbers"
COUPON_EXPIRED_404 = "This Coupon is Expired! Please Try some Another Coupon-Code."
PASSWORD_MISMATCH_401 = "Password does not Match! Please Try Again!!!"
PASSWORD_FORMAT_401 = "Password Must be 8 characters Long Password. Must contain at-least 1 Uppercase, 1 lowercase, and 1 special character."
INCORRECT_CREDENTIALS_404 = "Invalid Credentials"
INCORRECT_PASSWORD_404 = "Incorrect Password"
INCORRECT_TOKEN_404 = "Incorrect Token! Please Provide Correct Token."
CART_EMPTY_404 = "No Items found in your Cart. Please add items to your Cart."
SHIPPING_UNAVAILABLE_404 = "Please Provide Your Shipping Info. And proceed with Payment"
USER_NOT_FOUND = "User Not Found"
RECORD_NOT_FOUND = "No Records Found!!!"
TOKEN_SENT = "Reset Token Already Sent!"
OUT_OF_STOCK = "Out of Stock"


def Product_Not_Found_404(msg):
    """
    Product Not Found Error Message
    Parameters
    ----------------------------------------------------------
    msg: str - Error Message
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: str - Message Info
    """
    return f"Item with ID: ({msg}) NOT EXISTS!!!"


def Email_exists_409(email):
    """
    Email Exists Message when Registration Takes Place.
    Parameters
    ----------------------------------------------------------
    email: str - Email entered
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: str - Message Info
    """
    return f"{email} Already Exists. Please Try Another Email-ID"


def Stock_Unavailable_404(quantity):
    """
    Stock Not Available when User Search for any Products in Grocery.
    Parameters
    ----------------------------------------------------------
    quantity: int - Quantity of Products wanted
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: str - Message status
    """
    return f"Stock UnAvailable! {quantity} Stocks left."
