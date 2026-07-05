from datetime import date

from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str


class BookRead(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
