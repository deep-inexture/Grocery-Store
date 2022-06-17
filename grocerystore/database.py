from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Below function will load the required Environment variable to use anywhere in particular file.
load_dotenv()

# Connecting to Database using env variable which stores database URL.
engine = create_engine(os.environ.get('DB_URL'), echo=True)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


# Following function can be called everytime to initialize db variable and use while firing query.
def get_db():
    """
    This Method provides variable db which has access to all models section column names.
    Thus, it passes query to database and acts as its object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
