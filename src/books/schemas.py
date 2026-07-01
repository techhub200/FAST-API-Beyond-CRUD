from pydantic import BaseModel
from datetime import date

class BookType (BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
