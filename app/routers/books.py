from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.services.books_service import (
    get_books,
    get_book_by_id,
    create_book,
    update_book,
    delete_book,
    filter_books_by_author_and_theme,
    get_books_sorted_by_field,
)
from app.schemas.books import BookCreate, Book

router = APIRouter()

@router.get("/", response_model=list[Book])
async def read_books(db: AsyncSession = Depends(get_db)):
    """Retrieve all books."""
    return await get_books(db)

@router.get("/{book_id}", response_model=Book)
async def read_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a book by its ID."""
    book = await get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=Book)
async def add_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    """Add a new book."""
    return await create_book(db, book)

@router.put("/{book_id}", response_model=Book)
async def update_book_endpoint(book_id: int, book: BookCreate, db: AsyncSession = Depends(get_db)):
    """Update a book by its ID."""
    updated_book = await update_book(db, book_id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/{book_id}")
async def delete_book_endpoint(book_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a book by its ID."""
    if not await delete_book(db, book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}

@router.get("/search/", response_model=list[Book])
async def search_books(
    author: str = Query(None, description="Author of the book"),
    theme: str = Query(None, description="Theme of the book"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, gt=0, le=100, description="Maximum number of records to retrieve"),
    db: AsyncSession = Depends(get_db)
):
    """Search books by author and theme."""
    query = select(Book)
    if author:
        query = query.where(Book.author == author)
    if theme:
        query = query.where(Book.theme == theme)
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    books = result.scalars().all()
    if not books:
        raise HTTPException(status_code=404, detail="No books found with the given criteria")
    return books

@router.put("/update_publisher/")
async def update_books_publisher(
    book_id: int, new_publisher: str, db: AsyncSession = Depends(get_db)
):
    """Update the publisher of a book."""
    async with db.begin():
        book_to_update = await db.get(Book, book_id)
        if not book_to_update:
            raise HTTPException(status_code=404, detail="Book not found with the given ID")
        book_to_update.publisher = new_publisher
        await db.commit()
    return {"detail": "Book updated successfully"}

from sqlalchemy.sql import func

@router.get("/count_by_topic/", response_model=list[dict])
async def count_books_by_topic(db: AsyncSession = Depends(get_db)):
    """Count the number of books grouped by their topic."""
    query = select(Book.theme, func.count(Book.id).label("book_count")).group_by(Book.theme)
    result = await db.execute(query)
    count_by_topic = result.all()
    if not count_by_topic:
        raise HTTPException(status_code=404, detail="No books found")
    return count_by_topic
