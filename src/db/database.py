
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import declarative_base

from src.config import SessionLocal, engine

Base = declarative_base()

#table in postgres database
class Book(Base):
    __tablename__ = "BOOK_TABLE"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publisher = Column(String, nullable=False)
    published_date = Column(Date, nullable=False)
    page_count = Column(Integer, nullable=False)
    language = Column(String, nullable=False)





def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)