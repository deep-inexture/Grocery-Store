import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import re
import uuid
from ..repository import emailUtil, messages, emailFormat
from .. import models, tokens
from ..hashing import Hash

"""
This File does all validations related stuff for Login, Register, & Forgot Password.
All Database query stuff also takes place here.
"""


def register(request, db: Session):
    """
    Function provides validation and authentication before registering for endpoint.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    request: Schemas Object - Fetch key data to fetch values from user
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Registered Data of the user
    """
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(status_code=409, detail=messages.Email_exists_409(request.email))
    if not re.fullmatch(r"^[a-z\d]+[\._]?[a-z\d]+[@]\w+[.]\w{2,3}$", request.email):
        raise HTTPException(status_code=401, detail=messages.INVALID_EMAIL_401)
    if request.password != request.confirm_password:
        raise HTTPException(status_code=401, detail=messages.PASSWORD_MISMATCH_401)
    if not re.fullmatch(r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$', request.password):
        raise HTTPException(status_code=401, detail=messages.PASSWORD_FORMAT_401)

    new_user = models.User(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    user_id = db.query(models.User.id).filter(models.User.email == request.email).first()
    user_wallet = models.MyWallet(user_id=user_id[0])
    db.add(user_wallet)
    db.commit()
    db.refresh(user_wallet)

    return messages.json_status_response(200, "User Registered Successfully")


def login(request, db: Session):
    """
    Check Validation and password along with token to let access to other endpoints.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    request: Schemas Object - Fetch data for login requirements
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Access and Refresh Tokens
    """
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.INCORRECT_CREDENTIALS_404)
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.INCORRECT_PASSWORD_404)

    access_token = tokens.create_access_token(data={"sub": user.email})
    refresh_token = tokens.create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"}


def new_access_token(email):
    """
    Create New Access Token from Refresh Token and replace with Access Token
    Parameters
    ----------------------------------------------------------
    email: str - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Generates new access token from refresh token
    """
    access_token = tokens.create_access_token(data={"sub": email})
    return {'new_access_token': access_token}


def forgot_password(request, db: Session):
    """
    Function request email of user to provide token for reset password access link.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    request: Schemas Object - Contains data to fetch email
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Receive Email Message status/Confirmation
    """
    user = db.query(models.User).filter(models.User.email == request.email).first()
    existing_user = db.query(models.ResetCode).filter(models.ResetCode.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND)
    if existing_user:
        raise HTTPException(status_code=409, detail=messages.TOKEN_SENT)

    """Create Reset Token and save in Database"""
    reset_code = str(uuid.uuid1())
    new_code = models.ResetCode(email=request.email, reset_code=reset_code, expired_in=datetime.datetime.now())
    db.add(new_code)
    db.commit()
    db.refresh(new_code)

    """Formatting Email"""
    subject, recipient, message = emailFormat.forgotPasswordFormat(request.email, reset_code)

    """Sending Email to User"""
    emailUtil.send_email(subject, recipient, message)
    return messages.json_status_response(200, "We have send an Email, to reset your Password.")


def reset_password(reset_token, request, db: Session):
    """
    Request for new token and new password validations before reset the old password with new.
    Parameters
    ----------------------------------------------------------
    reset_token: str - Token generated on email to check user presence in db.
    db: Database Object - Fetching Schemas Content
    request: Schemas Object - Contains Token and Password Keys
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch data for Password Update Confirmation
    """
    user = db.query(models.ResetCode).filter(models.ResetCode.reset_code == reset_token).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.INCORRECT_TOKEN_404)
    if request.password != request.confirm_password:
        raise HTTPException(status_code=401, detail=messages.PASSWORD_MISMATCH_401)
    if not re.fullmatch(r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$', request.password):
        raise HTTPException(status_code=401, detail=messages.PASSWORD_FORMAT_401)

    email = getattr(user, 'email')

    check_user = db.query(models.User).filter(models.User.email == email).first()
    check_user.password = Hash.bcrypt(request.password)

    delete_token = db.query(models.ResetCode).filter(models.ResetCode.email == email).first()
    db.delete(delete_token)

    db.commit()
    return messages.json_status_response(200, "Your Password has been Successfully Reset.")
