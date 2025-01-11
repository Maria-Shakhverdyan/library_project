from sqlalchemy import Column, Integer, String, Index, Text
from app.database.connection import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(Text, nullable=False)  # Должно быть строкой
    publisher = Column(String, nullable=True)
    theme = Column(Text, nullable=True)    # Должно быть строкой

Index("idx_books_title", Book.title)