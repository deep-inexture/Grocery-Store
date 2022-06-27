def forgotPasswordFormat(email, reset_code):
    subject = "Hello User"
    recipient = email
    message = """
        <!DOCTYPE html>
        <html>
        <title>Reset Password</title>
        <body>
        <h3>Hello, {0:}</h3>
        <p>Password Reset Request has been received by Someone.</p>
        <p>Your Token to Reset Password :<u>{1}</u></p>
        <p>If you did not requested, You can ignore this mail!<p>
        </body>
        </html>
        """.format(email, reset_code)
    return subject, recipient, message


def invoiceFormat(email, invoice, shipping_info, items, discount):
    subject = "Grocery Store - Order Invoice"
    recipient = email
    message = """
        <!DOCTYPE html>
        <html>
        <title>Invoice</title>
        <body>
        <h3>Hello, {0:}</h3>
        *********************************************************************<br>
        INVOICE<br>
        *********************************************************************<br>
        <table border="0">
        <tr>
            <td>ORDER ID:                   </td>
            <td>{1}</td>
        </tr>
        <tr>
            <td>TOTAL ITEMS:                </td>
            <td>{9}</td>
        </tr>
        <tr>
            <td>ORDER AMOUNT:               </td>
            <td>{2}</td>
        </tr>
        <tr>
            <td>DISCOUNT APPLIED:           </td>
            <td>{10}%</td>
        </tr>
        <tr>
            <td>ORDER SHIPPING INFO:        </td>
            <td>{5}, {6}, {7}</td>
        </tr>
        <tr>
            <td>PHONE NO.:                  </td>
            <td>{8}</td>
        </tr>
        <tr>
            <td>ORDER STATUS:               </td>
            <td>{3}</td>
        </tr>
        </table>
        *********************************************************************<br>
        <p>{4}</p>
        <br><br>
        Regards,<br> 
        Grocery Store
        </body>
        </html>
        """.format(email, invoice['id'], (invoice['amount']/100), invoice['status'], invoice['notes'][0],
                   getattr(shipping_info, "address"), getattr(shipping_info, "city"), getattr(shipping_info, "state"),
                   getattr(shipping_info, "phone_no"), items, discount)
    return subject, recipient, message
