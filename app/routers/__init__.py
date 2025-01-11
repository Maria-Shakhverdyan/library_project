from fastapi import APIRouter
from app.routers import books, readers, loans

api_router = APIRouter()
api_router.include_router(books.router, prefix="/books", tags=["Books"])
api_router.include_router(readers.router, prefix="/readers", tags=["Readers"])
api_router.include_router(loans.router, prefix="/loans", tags=["Loans"])