
from sqlalchemy import create_engine #Imports the SQLAlchemy function used to create a connection to the database.
from sqlalchemy.orm import sessionmaker  #Imports SQLAlchemy’s session factory, which helps create database sessions for queries.

DATABASE_URL = "postgresql+psycopg://postgres:Postgre%402004@localhost:5432/BOOK_DATABASE"

engine = create_engine(DATABASE_URL, echo=True)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)