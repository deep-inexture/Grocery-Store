from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, database, oauth2
from ..repository import authentication

"""
It includes Authentication routers for both User & Admin. First Point Router Before Handing any other
routing processes.
"""


router = APIRouter(
    tags=["Authentication"]
)
get_db = database.get_db


@router.post('/register')
def registration(request: schemas.UserRegister, db: Session = Depends(get_db)):
    """
    Registration User Authentication Requirements
    Call Register function in repository directory to validate credentials & validations.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    request: Schemas Object - Fetch key data to fetch values from user
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Registered Data of the user
    """
    return authentication.register(request, db)


@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(get_db)):
    """
    Login Process for both Admin and User.
    Call Login function in repository directory to validate credentials and provide access token.
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    request: Schemas Object - Fetch data for login requirements
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Fetch Access and Refresh Tokens
    """
    return authentication.login(request, db)


@router.get('/new_access_token')
def new_access_token(current_user: schemas.User = Depends(oauth2.get_current_user_access_token)):
    """
    Router to Create New Access Token by taking Refresh Token
    Parameters
    ----------------------------------------------------------
    current_user: User Object - Current Logged-In User Session
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Generates new access token from refresh token
    """

    return authentication.new_access_token(current_user.email)


@router.post('/forgot_password')
def forgot_password(request: schemas.ForgotPassword, db: Session = Depends(get_db)):
    """
    Check User Existence
    Parameters
    ----------------------------------------------------------
    db: Database Object - Fetching Schemas Content
    request: Schemas Object - Contains data to fetch email
    ----------------------------------------------------------

    Returns
    ----------------------------------------------------------
    response: json object - Receive Email Message status/Confirmation
    """
    return authentication.forgot_password(request, db)


@router.post('/reset_password/{reset_token}')
def reset_password(reset_token: str, request: schemas.ResetPassword, db: Session = Depends(get_db)):
    """
    Reset Password using token Sent via Mail
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
    return authentication.reset_password(reset_token, request, db)
