
from sqlalchemy import create_engine  # Imports the SQLAlchemy function used to create a connection to the database.
from sqlalchemy.orm import sessionmaker  # Imports SQLAlchemy’s session factory.

from dotenv import load_dotenv  # Loads environment variables from a .env file.
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
engine = create_engine(DATABASE_URL, echo=True)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


