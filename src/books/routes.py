
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from src.auth.dependencies import Access_Token_Bearer
from src.books.schemas import BookCreate, BookRead
from src.db.database import Book, get_db

book_router = APIRouter()
access_token_bearer = Access_Token_Bearer()


# Get all books
@book_router.get("/", response_model=list[BookRead])
async def retrieve_books(db: Session = Depends(get_db),user_details: dict = Depends(access_token_bearer)):
    return db.query(Book).all()


# Get book by ID
@book_router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, db: Session = Depends(get_db),user_details: dict = Depends(access_token_bearer)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return book

# Create a new book
@book_router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: Session = Depends(get_db),user_details: dict = Depends(access_token_bearer)):
    db_book = Book(
        title=book.title,
        author=book.author,
        publisher=book.publisher,
        published_date=book.published_date,
        page_count=book.page_count,
        language=book.language,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book




# Update a book
@book_router.put("/{book_id}", response_model=BookRead)
async def update_book(book_id: int, updated_book: BookCreate, db: Session = Depends(get_db),user_details: dict = Depends(access_token_bearer)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    book.title = updated_book.title
    book.author = updated_book.author
    book.publisher = updated_book.publisher
    book.published_date = updated_book.published_date
    book.page_count = updated_book.page_count
    book.language = updated_book.language
    db.commit()
    db.refresh(book)
    return book


# Delete a book
@book_router.delete("/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db),user_details: dict = Depends(access_token_bearer)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}