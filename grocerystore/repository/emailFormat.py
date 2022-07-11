import os
from dotenv import load_dotenv

"""
Collection of Email Structures. ForgotPassword Links Format and Order Invoice Format.
"""

load_dotenv()


def forgotPasswordFormat(email, reset_code):
    """
    Structure for Forgot Password Reset Link.
    Parameters
    ----------------------------------------------------------
    reset_code: str - Token to reset Password
    email: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: str - Mail Body
    """
    DB_URL = os.environ.get('SITE_URL')
    subject = "Hello User"
    recipient = email
    message = """
        <!DOCTYPE html>
        <html>
        <title>Reset Password</title>
        <body>
        <h3>Hello, {0:}</h3>
        <p>Password Reset Request has been received by Someone.</p>
        <p>Visit Below Link to Reset Your Password<br><u>{2}/{1}</u></p>
        <p>If you did not requested, You can ignore this mail!<p>
        </body>
        </html>
        """.format(email, reset_code, DB_URL)
    return subject, recipient, message


def invoiceFormat(email, invoice, shipping_info, items, discount, amount):
    """
    Email Structure to Send Product Invoice to User
    Parameters
    ----------------------------------------------------------
    invoice: dict - Order Invoice Generated
    email: User Object - Current Logged-In User Session
    shipping_info: dict - User Address Info
    items: int - Total no of Items Ordered
    discount: int - Total applicable Discount
    amount: float - Total Payable Amount
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: str - Mail Body
    """
    subject = "Grocery Store - Order Invoice"
    recipient = email
    message = f"""
        <!DOCTYPE html>
        <html>
        <title>Invoice</title>
        <body>
        <h3>Hello, {email}:</h3>
        <hr>
        INVOICE<br>
        <hr>
        <table border="0">
        <tr>
            <td>ORDER ID:                   </td>
            <td>{invoice['id']}</td>
            <td></td>
        </tr>
        <tr>
            <td>ITEMS:                </td>
            <td>"""
    for i in items:
        item_name = getattr(i, "product_name")
        message = message + item_name + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        item_quantity = getattr(i, "product_quantity")
        message = message + str(item_quantity) + " Nos.<br>"

    message = message + """</td></tr>
        <tr>
            <td>ORDER AMOUNT:               </td>
            <td>{2}</td>
            <td></td>
        </tr>
        <tr>
            <td>DISCOUNT APPLIED:           </td>
            <td>{9}%</td>
            <td></td>
        </tr>
        <tr>
            <td>ORDER SHIPPING INFO:        </td>
            <td>{5}, {6}, {7}</td>
            <td></td>
        </tr>
        <tr>
            <td>PHONE NO.:                  </td>
            <td>{8}</td>
            <td></td>
        </tr>
        <tr>
            <td>ORDER STATUS:               </td>
            <td>{3}</td>
            <td></td>
        </tr>
        <tr>
            <td>PAYMENT LINK:               </td>
            <td>{10}</td>
            <td></td>
        </tr>
        </table>
        <hr>
        <p>{4}</p>
        <br><br>
        Regards,<br> 
        Grocery Store
        </body>
        </html>
        """.format(email, invoice['id'], amount, invoice['payment_status'], 'Thank You! Please Visit Again...',
                   getattr(shipping_info, "address"), getattr(shipping_info, "city"), getattr(shipping_info, "state"),
                   getattr(shipping_info, "phone_no"), discount, invoice['url'])
    return subject, recipient, message
