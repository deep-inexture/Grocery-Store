import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Below function will load the required Environment varaible to use anywhere in particular file.
load_dotenv()

# Connecting to Database using env variable which stores database URL.
# engine = sqlalchemy.create_engine(os.environ.get('DATABASE_URL_POSTGRES'), echo=True)
engine = create_engine(os.environ.get('LOCAL_DATABASE_URL'), echo=True)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Following function can be called everytime to initialize db varaible and use while fireing query.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
