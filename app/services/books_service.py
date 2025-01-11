from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models.books import Book
from app.schemas.books import BookCreate


async def get_books(db: AsyncSession):
    """Получение всех книг."""
    result = await db.execute(select(Book))
    return result.scalars().all()

async def get_book_by_id(db: AsyncSession, book_id: int):
    """Получение книги по ID."""
    result = await db.execute(select(Book).where(Book.id == book_id))
    return result.scalar()

async def create_book(db: AsyncSession, book: BookCreate):
    """Создание новой книги."""
    new_book = Book(**book.dict())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

async def update_book(db: AsyncSession, book_id: int, book: BookCreate):
    """Обновление книги по ID."""
    existing_book = await get_book_by_id(db, book_id)
    if not existing_book:
        return None
    for key, value in book.dict().items():
        setattr(existing_book, key, value)
    await db.commit()
    await db.refresh(existing_book)
    return existing_book

async def delete_book(db: AsyncSession, book_id: int):
    """Удаление книги по ID."""
    existing_book = await get_book_by_id(db, book_id)
    if not existing_book:
        return False
    await db.delete(existing_book)
    await db.commit()
    return True

#SELECT...WHERE
async def filter_books_by_author_and_theme(db: AsyncSession, author: str, theme: str):
    """
    Фильтрация книг по автору и теме.
    """
    # Отладочный вывод
    print(f"Filtering books by author='{author}', theme='{theme}'")

    # Выполнение запроса
    result = await db.execute(
        select(Book).where(Book.author == author, Book.theme == theme)
    )

    # Получение результатов
    books = result.scalars().all()
    print(f"Found books: {books}")
    return books

#Сортировка списка книг по указанному полю
async def get_books_sorted_by_field(db: AsyncSession, sort_by: str):
    valid_sort_fields = ["title", "author", "publisher", "theme"]
    if sort_by not in valid_sort_fields:
        raise ValueError(f"Invalid sort field: {sort_by}")
    result = await db.execute(select(Book).order_by(getattr(Book, sort_by)))
    return result.scalars().all()