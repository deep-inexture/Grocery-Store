import datetime
from . import emailUtil
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, token
from ..hashing import Hash
import re
import uuid


def register(request, db: Session):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(status_code=409, detail=f"{request.email} Already Exists. Please Try Another Email-ID")
    if not re.fullmatch(r"^[a-z\d]+[\._]?[a-z\d]+[@]\w+[.]\w{2,3}$", request.email):
        raise HTTPException(status_code=401, detail=f"Invalid Email-ID Format!!!")
    if request.password != request.confirm_password:
        raise HTTPException(status_code=401, detail=f"Password does not Match! Please Try Again!!!")
    if not re.fullmatch(r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$', request.password):
        raise HTTPException(status_code=401,
                            detail="Password Must be 8 characters Long Password. Must contain at-least 1 Uppercase, 1 lowercase, and 1 special character.")

    new_user = models.User(username=request.username, email=request.email, password=Hash.bcrypt(request.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login(request, db: Session):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")

    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


def forgot_password(request, db: Session):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    existing_user = db.query(models.ResetCode).filter(models.ResetCode.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User Not Found")
    if existing_user:
        raise HTTPException(status_code=409, detail=f"Reset Token Already Sent!")

    """Create Reset Token and save in Database"""
    reset_code = str(uuid.uuid1())
    new_code = models.ResetCode(email=request.email, reset_code=reset_code, expired_in=datetime.datetime.now())
    db.add(new_code)
    db.commit()
    db.refresh(new_code)

    """Sending Email to User"""
    subject = "Hello User"
    recipient = [request.email]
    message = """
    <!DOCTYPE html>
    <html>
    <title>Reset Password</title>
    <body>
    <h1>Hello, {0:}</h1>
    <p>Password Reset Request has been received by Someone.</p>
    <br>
    <p>Your Token to Reset Password :{1}</p>
    <br>
    <p>If you did not requested, You can ignore this mail!<p>
    </body>
    </html> 
    """.format(request.email, reset_code)

    emailUtil.send_email(subject, recipient, message)
    return {
        "reset_code": reset_code,
        "message": "We have send an Email, to reset your Password."
    }


def reset_password(request, db: Session):
    user = db.query(models.ResetCode).filter(models.ResetCode.reset_code == request.token).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Token!!!")
    if request.password != request.confirm_password:
        raise HTTPException(status_code=401, detail=f"Password does not Match! Please Try Again!!!")
    if not re.fullmatch(r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$', request.password):
        raise HTTPException(status_code=401,
                            detail="Password Must be 8 characters Long Password. Must contain at-least 1 Uppercase, 1 lowercase, and 1 special character.")

    email = getattr(user, 'email')

    check_user = db.query(models.User).filter(models.User.email == email).first()
    check_user.password = Hash.bcrypt(request.password)

    delete_token = db.query(models.ResetCode).filter(models.ResetCode.email == email).first()
    db.delete(delete_token)

    db.commit()
    return {"message": "Your Password has been Successfully Reset."}
