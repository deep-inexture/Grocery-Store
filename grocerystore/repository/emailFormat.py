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


def invoiceFormat(email, invoice):
    subject = "Hello User"
    recipient = email
    message = """
        <!DOCTYPE html>
        <html>
        <title>Invoice</title>
        <body>
        <h3>Hello, {0:}</h3>
        *************************************<br>
        INVOICE<br>
        *************************************<br>
        <p>ID: {1}<p>
        <p>Amount: {2}</p>
        <p>Status: {3}</p>
        <p>{4}</p>
        *************************************<br>
        
        Regards,<br> 
        Grocery Store
        </body>
        </html>
        """.format(email, invoice['id'], (invoice['amount']/100), invoice['status'], invoice['notes'][0])
    return subject, recipient, message
