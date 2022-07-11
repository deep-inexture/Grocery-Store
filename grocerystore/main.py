from fastapi import FastAPI
from . import models
from .database import engine
from .routers import admin, authentication, users
from fastapi.staticfiles import StaticFiles

"""
Creates an Object of FastAPI Instance as app with some Title and Description while viewing in
Swagger or ReadDoc mode.
"""

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Operations with Authentication. It Consists of Registration | Login |"
                       " Forgot Password"
    },
    {
        "name": "Admin",
        "description": "Operations with Admin. It Consists of Products - CRUD | Orders Details | "
                       "Discount Coupons Metadata",
    },
    {
        "name": "User",
        "description": "Operations with users. It Consists of Products | Cart | Wallet | Orders | Invoice",
    },
]

app = FastAPI(
    title='Grocery Store',
    description='FastAPI Implemented Grocery Store System',
    version='1.0.0',
    terms_of_service='http://grocery-store-development.herokuapp.com/docs',
    contact={
        'name': 'DEEP SHAH',
        'email': 'deep.inexture@gmail.com'
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata
)

"""Allow Static Files to use in app via mounting"""
app.mount("/templates", StaticFiles(directory="grocerystore/templates", html=True), name="templates")

"""Following command will create new tables if not exists in Database."""
"""Now We are using alembic migrations."""
models.Base.metadata.create_all(engine)


"""Following command will call the routers and stored in different files for clean flow of project ."""
app.include_router(authentication.router)
app.include_router(admin.router)
app.include_router(users.router)

"""
Using following we can directly run python file instead of whole uvicorn command.
Don't use while of production server.
"""
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
