from fastapi import FastAPI

from src.auth.auth_routes import auth_router
from src.books.routes import book_router


app = FastAPI(
    title="BOOKlY",
    description="RESAPI for BookDEsign",
)

app.include_router(book_router, prefix="/api/books", tags=["books"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
