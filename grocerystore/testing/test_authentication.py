import json
import os
from dotenv import load_dotenv

load_dotenv()

"""
Below are Registration Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 4 Nos

test_registration_success_200: Successful User Registration      : 200
test_registration_email_exists_409: Email-ID Already Exists      : 409
test_registration_invalid_email_401: Invalid Email-ID Format     : 401
test_registration_password_mismatch_401: Password Mismatch Error : 401
test_registration_password_format_401: Incorrect Password Format : 401
"""
"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""


def test_registration_success_200(client):
    data = {
        "username": os.environ.get('username'),
        "email": os.environ.get('email'),
        "password": os.environ.get('password'),
        "confirm_password": os.environ.get('confirm_password')
    }
    response = client.post('/register', json.dumps(data))
    assert response.status_code == 200
    assert response.json()["username"] == os.environ.get('username')
    assert response.json()["email"] == os.environ.get('email')


def test_registration_email_exists_409(client):
    data = {
        "username": os.environ.get('username'),
        "email": os.environ.get('email'),
        "password": os.environ.get('password'),
        "confirm_password": os.environ.get('confirm_password')
    }
    response = client.post('/register', json.dumps(data))
    assert response.status_code == 409
    assert "Email Already Exists"


def test_registration_invalid_email_401(client):
    data = {
        "username": os.environ.get('username'),
        "email": "Invalid-Email-Format",
        "password": os.environ.get('password'),
        "confirm_password": os.environ.get('confirm_password')
    }
    response = client.post('/register', json.dumps(data))
    assert response.status_code == 401
    assert "Invalid Email-ID Format"


def test_registration_password_mismatch_401(client):
    data = {
        "username": "TestUserSample",
        "email": "TestUserSample@gmail.com",
        "password": "TestUser@12345",
        "confirm_password": "TestUser@1234"
    }
    response = client.post('/register', json.dumps(data))
    assert response.status_code == 401
    assert "Password Does Not Match"


def test_registration_password_format_401(client):
    data = {
        "username": "TestUserSample",
        "email": "TestUserSample@gmail.com",
        "password": 'password',
        "confirm_password": 'password'
    }
    response = client.post('/register', json.dumps(data))
    assert response.status_code == 401
    assert "Invalid Password Format."


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
Below are Login Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 2 Nos

test_login_success_200: Successful User Login                    : 200
test_login_incorrect_credentials_404: Incorrect Credentials      : 404
test_login_incorrect_password_404: Incorrect Password            : 404
"""


def test_login_success_200(client):
    data = {
        "username": os.environ.get('email'),
        "password": os.environ.get('password'),
    }
    response = client.post('/login', json.dumps(data))
    assert response.status_code == 200
    assert "access_token: {}, refresh_token: {}, token_type: bearer"


def test_login_incorrect_credentials_404(client):
    data = {
        "username": "unknown@user.in",
        "password": "UnknownUser@1234"
    }
    response = client.post('/login', json.dumps(data))
    assert response.status_code == 404
    assert "User Not Found"


def test_login_incorrect_password_404(client):
    data = {
        "username": os.environ.get('email'),
        "password": "User@12345"
    }
    response = client.post('/login', json.dumps(data))
    assert response.status_code == 404
    assert "Incorrect Password! Please Try Again"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
Below are Forgot Password Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 2 Nos

test_forgot_password_200: Email-IS Exists & Token Sent Success   : 200
test_forgot_password_user_not_found_404: User Not Found          : 404
test_forgot_password_token_sent_404: Token Already Sent          : 404
"""


def test_forgot_password_200(client):
    data = {
        "email": os.environ.get('email'),
    }
    response = client.post('/forgot_password', json.dumps(data))
    assert  response.status_code == 200
    assert response.json()["message"]


def test_forgot_password_user_not_found_404(client):
    data = {
        "email": "shahdeep1908@gmail.com"
    }
    response = client.post('/forgot_password', json.dumps(data))
    assert  response.status_code == 404
    assert "User Not Found"


def test_forgot_password_token_sent_404(client):
    data = {
        "email": os.environ.get('email'),
    }
    response = client.post('/forgot_password', json.dumps(data))
    assert  response.status_code == 409
    assert "Token Already Sent"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
Below are Forgot Password Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 2 Nos

test_reset_password_200: Token is Correct & password has Reset   : 200
test_reset_password_incorrect_token_404: Incorrect Token Entered : 404
test_reset_password_password_mismatch_404: New Password Mismatch : 404
"""


def test_reset_password_200(client):
    data = {
        "password": os.environ.get('password'),
        "confirm_password": os.environ.get('confirm_password')
    }
    response = client.post('/reset_password/2d6854ae-f849-11ec-b20b-1f975712687d', json.dumps(data))
    assert response.status_code == 200
    assert response.json()["message"]


def test_reset_password_incorrect_token_404(client):
    data = {
        "password": os.environ.get('password'),
        "confirm_password": os.environ.get('confirm_password')
    }
    response = client.post('/reset_password/incorrect_token', json.dumps(data))
    assert response.status_code == 404
    assert "Incorrect Token"


def test_reset_password_password_mismatch_404(client):
    data = {
        "password": "Test@1234",
        "confirm_password": os.environ.get('confirm_password')
    }
    response = client.post('/reset_password/2d6854ae-f849-11ec-b20b-1f975712687d', json.dumps(data))
    assert response.status_code == 404
    assert "Password Mismatch"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
