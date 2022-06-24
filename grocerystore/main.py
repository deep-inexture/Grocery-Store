from fastapi import FastAPI
from . import models
from .database import engine
from .routers import admin, authentication, users

# Creates an Object of FastAPI Instance as app with some Title and Description while viewing in
# Swagger or ReadDoc mode.
app = FastAPI(
    title='Grocery Store',
    description='FastAPI Implemented Grocery Store System'
)

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
