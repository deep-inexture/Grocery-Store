import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

engine = sqlalchemy.create_engine(os.environ.get('DATABASE_URL'), echo=True)
# engine = create_engine(os.environ.get('LOCAL_DATABASE_URL'), echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
