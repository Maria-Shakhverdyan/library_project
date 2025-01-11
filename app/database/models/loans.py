from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    issue_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=False)
    description = Column(String, nullable=True)  # Новое поле

    book = relationship("Book", backref="loans")
    reader = relationship("Reader", backref="loans")

