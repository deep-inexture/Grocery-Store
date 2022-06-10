from fastapi import FastAPI
from . import models
from .database import engine
from .routers import admin, authentication

app = FastAPI(
    title='Grocery Store',
    description='FastAPI Implemented Grocery Store System'
)
models.Base.metadata.create_all(engine)


app.include_router(authentication.router)
app.include_router(admin.router)


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)