from fastapi import FastAPI
from src.books.routes import book_router
app=FastAPI()

version ="V1"

app = FastAPI(
    title="BOOKlY",
    description="RESAPI for BookDEsign",
    version=version
)

app.include_router(  book_router,
    prefix=f"/api/{version}/books",
    tags=["books"])