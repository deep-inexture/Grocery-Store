from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from dotenv import load_dotenv
import os
from typing import List
from starlette.responses import JSONResponse

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
    MAIL_FROM=os.environ.get('MAIL_FROM'),
    MAIL_PORT=os.environ.get('MAIL_PORT'),
    MAIL_SERVER=os.environ.get('MAIL_SERVER'),
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)


def send_email(subject: str, recipient: List, message: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipient,
        body=message,
        subtype="html"
    )
    fm = FastMail(conf)
    fm.send_message(message)
    return True
