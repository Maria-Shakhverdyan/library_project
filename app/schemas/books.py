from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    """Базовая схема для книги."""
    title: str
    author: str
    publisher: Optional[str] = None
    theme: Optional[str] = None


class Book(BookBase):
    """Схема для представления книги."""
    id: int

    class Config:
        from_attributes = True


class BookCreate(BookBase):
    """Схема для создания книги."""
    pass