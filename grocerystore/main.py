from fastapi import FastAPI
import uvicorn
from . import models, schemas
from .database import engine
from .routers import admin, authentication

app = FastAPI()
models.Base.metadata.create_all(engine)


app.include_router(authentication.router)
app.include_router(admin.router)


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)