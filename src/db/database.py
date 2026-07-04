
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import engine

Base = declarative_base()


class Book(Base):
    __tablename__ = "BOOK_TABLE"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)