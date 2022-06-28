import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

"""
Email Sending Background Processes and Information via smtplib and email.
"""


def send_email(subject, to, text):
    """
    Function Call when Email process execution takes place.
    """
    try:
        load_dotenv()
        MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
        MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
        MAIL_PORT = os.environ.get('MAIL_PORT')
        MAIL_SERVER = os.environ.get('MAIL_SERVER')

        """Defining The Message"""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = MAIL_USERNAME
        msg["To"] = to

        part = MIMEText(text, "html")
        msg.attach(part)

        context = ssl.create_default_context()
        """Create your SMTP session"""
        with smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT, context=context) as server:
            # User Authentication
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            """Sending the Email"""
            server.sendmail(
                MAIL_USERNAME, to, msg.as_string()
            )

    except Exception as ex:
        print("Something went wrong....", ex)
