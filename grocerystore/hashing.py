from passlib.context import CryptContext

"""
This files generates Hash value of each password for protection of User Data and forward
back to Authentication File that stores bcrypt password in Database.
Password again come here to verify the bcrypt password is correct or not.
"""

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    def verify(hashed_pwd, plain_pwd):
        return pwd_cxt.verify(plain_pwd, hashed_pwd)
