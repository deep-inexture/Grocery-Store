from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import schemas, database, oauth2
from repository import authentication


# It includes Authentication routers for both User & Admin

router = APIRouter(
    tags=["Authentication"]
)
get_db = database.get_db


@router.post('/register', response_model=schemas.User)
def registration(request: schemas.UserRegister, db: Session = Depends(get_db)):
    """
    Registration User Authentication Requirements
    Call Register function in repository directory to validate credentials & validations.
    """
    return authentication.register(request, db)


@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(get_db)):
    """
    Login Process for both Admin and User.
    Call Login function in repository directory to validate credentials and provide access token.
    """
    return authentication.login(request, db)


@router.get('/new_access_token')
def new_access_token(current_user: schemas.User = Depends(oauth2.get_current_user_access_token)):
    """Router to Create New Access Token by taking Refresh Token"""
    return authentication.new_access_token(current_user.email)


@router.post('/forgot_password')
def forgot_password(request: schemas.ForgotPassword, db: Session = Depends(get_db)):
    """Check User Existence"""
    return authentication.forgot_password(request, db)


@router.post('/reset_password/{reset_token}')
def reset_password(reset_token: str, request: schemas.ResetPassword, db: Session = Depends(get_db)):
    """Reset Password using token Sent via Mail"""
    return authentication.reset_password(reset_token, request, db)
