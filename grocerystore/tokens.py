from datetime import datetime, timedelta
from jose import JWTError, jwt
from grocerystore import schemas
from dotenv import load_dotenv
import os

"""
Following file generates Token after each correct Authentication and need to re-login once 30 min
Expiry time is over.It is connected to oauth2 file where User gets stored as session variable.
"""

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
JWT_REFRESH_SECRET_KEY = os.environ.get('JWT_REFRESH_SECRET_KEY')


def create_access_token(data: dict):
    """
    Create Access Token using JWT and return encoded token to Login Section
    Parameters
    ----------------------------------------------------------
    data: dict - access Token
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: UTF-8 - encoded access Token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    """
    Re-Create Access Token from the Refresh Token in data dictionary.
    Parameters
    ----------------------------------------------------------
    data: dict - refresh Token
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: UTF-8 - new encoded access Token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """
    Once User gets login verify token using below method. And this code will be accessible for 30
    minutes.
    Parameters
    ----------------------------------------------------------
    token: str - access Token
    credentials_exception: exception - Invalid Exception Details
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: str - Token Data
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)

        return token_data
    except JWTError:
        raise credentials_exception


def verify_refresh_token(token: str, credentials_exception):
    """
    Once User apply for refresh token it automatically validates and provides new Access token.
    Parameters
    ----------------------------------------------------------
    token: str - refresh token
    credentials_exception: Exception - Invalid Credentials exception
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: str - token data
    """
    try:
        payload = jwt.decode(token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)

        return token_data
    except JWTError:
        raise credentials_exception
