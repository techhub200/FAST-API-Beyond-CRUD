from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

from src.config import engine

Base = declarative_base()

class BookType(Base):
    __tablename__ = "BOOK_TABLE"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    publisher = Column(String)
    published_date = Column(DateTime)
    page_count = Column(Integer)
    language = Column(String)

# This actually creates the table
Base.metadata.create_all(bind=engine)