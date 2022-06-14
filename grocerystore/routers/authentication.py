from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .. import schemas, database, models, token
from ..hashing import Hash
from sqlalchemy.orm import Session
import re


# It includes Authentication routers for both User & Admin

router = APIRouter(
    tags=["Authentication"]
)
get_db = database.get_db


@router.post('/register', response_model=schemas.User)
def registration(request: schemas.UserRegister, db: Session= Depends(get_db)):
    """
    Registration User Authentication Requirements
    """
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(status_code=409, detail=f"{request.email} Already Exists. Please Try Another Email-ID")
    if not re.fullmatch(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", request.email):
        raise HTTPException(status_code=401, detail=f"Invalid Email-ID Format!!!")
    if request.password != request.confirm_password:
        raise HTTPException(status_code=401, detail=f"Password does not Match! Please Try Again!!!")
    if not re.fullmatch(r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$', request.password):
        raise HTTPException(status_code=401, detail=f"Password Must be 8 characters Long Password Must contain "
                                                    f"at-east 1 Uppercase, 1 lowercase, and 1 special character.")

    new_user = models.User(username=request.username, email=request.email, password=Hash.bcrypt(request.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login Process for both Admin and User.
    """
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")

    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

