
from sqlalchemy import create_engine #acts as a bridge between python and SQLDATABASE
from sqlalchemy.orm import sessionmaker  #A Session is used to perform database operations.

DATABASE_URL = "postgresql+psycopg://postgres:Postgre%402004@localhost:5432/BOOK_DATABASE"

engine = create_engine(DATABASE_URL, echo=True)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)