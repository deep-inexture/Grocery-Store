NO_CHANGES_302 = "No Change Detected!"
NOT_AUTHORIZE_401 = "You are not Authorized to view this Page!"
INVALID_EMAIL_401 = "Invalid Email-ID Format!!!"
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
    return f"Item with ID: ({msg}) NOT EXISTS!!!"


def Email_exists_409(email):
    return f"{email} Already Exists. Please Try Another Email-ID"


def Stock_Unavailable_404(quantity):
    return f"Stock UnAvailable! {quantity} Stocks left."
