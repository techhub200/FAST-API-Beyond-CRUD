
from fastapi import APIRouter ,status
from fastapi.exceptions import HTTPException
from src.books.book_data import books
from src.books.schemas import BookType

book_router=APIRouter()

# Get all books
@book_router.get("/")
async def retrieve_books() ->list:
    return books


# Get book by ID
@book_router.get("/{book_id}")
async def get_book(book_id:int):
    for book in books:
        if book["id"] == book_id:
            return book;

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not found")


# Delete a book
@book_router.delete("/{book_id}")
async def delete_book(book_id: int):
    for  book in books:
        if book["id"] == book_id:
            deleted_book = books.pop(book)
            return {
                "message": "Book deleted successfully",
                "book": deleted_book
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )

# Create a new book
@book_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookType):
    books.append(book.model_dump())

    return {
        "message": "Book created successfully",
        "book": book
    }


# Update a book
@book_router.put("/{book_id}")
async def update_book(book_id: int, updated_book: BookType):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books[index] = updated_book.model_dump()
            return {
                "message": "Book updated successfully",
                "book": books[index]
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )


