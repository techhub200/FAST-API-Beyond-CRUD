
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.books.schemas import BookCreate, BookRead
from src.db.database import Book, get_db

book_router = APIRouter()


# Create a new book
@book_router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(title=book.title, author=book.author)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


# Get all books
@book_router.get("/", response_model=list[BookRead])
async def retrieve_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


# Get book by ID
@book_router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return book


# Update a book
@book_router.put("/{book_id}", response_model=BookRead)
async def update_book(book_id: int, updated_book: BookCreate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    book.title = updated_book.title
    book.author = updated_book.author
    db.commit()
    db.refresh(book)
    return book


# Delete a book
@book_router.delete("/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}