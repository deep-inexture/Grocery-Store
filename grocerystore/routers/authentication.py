from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, database
from ..repository import authentication
from sqlalchemy.orm import Session


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
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login Process for both Admin and User.
    Call Login function in repository directory to validate credentials and provide access token.
    """
    return authentication.login(request, db)


@router.post('/forgot_password')
def forgot_password(request: schemas.ForgotPassword, db: Session = Depends(get_db)):
    """Check User Existence"""
    return authentication.forgot_password(request, db)


@router.post('/reset_password')
def reset_password(request: schemas.ResetPassword, db: Session = Depends(get_db)):
    """Reset Password using token Sent via Mail"""
    return authentication.reset_password(request, db)
