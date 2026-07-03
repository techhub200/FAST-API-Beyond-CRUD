from fastapi import FastAPI
from src.books.routes import book_router
#from src.config import SessionLocal
#from src.db import database

app=FastAPI()


app = FastAPI(
    title="BOOKlY",
    description="RESAPI for BookDEsign",
    
)

app.include_router(  book_router,
    prefix=f"/api/books",
    tags=["books"])