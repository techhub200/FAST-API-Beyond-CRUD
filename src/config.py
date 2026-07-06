
from sqlalchemy import create_engine #Imports the SQLAlchemy function used to create a connection to the database.
from sqlalchemy.orm import sessionmaker  #Imports SQLAlchemy’s session factory, which helps create database sessions for queries.

from dotenv import load_dotenv  #Imports the load_dotenv function from the python-dotenv package, which loads environment variables from a .env file.
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)