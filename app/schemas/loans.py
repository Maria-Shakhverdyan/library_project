from pydantic import BaseModel
from typing import Optional
from datetime import date

class LoanBase(BaseModel):
    """Базовая схема для выдачи."""
    book_id: int
    reader_id: int
    issue_date: date
    due_date: date

class LoanCreate(LoanBase):
    """Схема для создания выдачи."""
    pass

class Loan(LoanBase):
    """Схема для представления выдачи."""
    id: int
    return_date: Optional[date] = None

    class Config:
        from_attributes = True

class LoanDetail(BaseModel):
    id: int
    book_title: str
    reader_name: str

    class Config:
        from_attributes = True

class LoanGroupByBook(BaseModel):
    book_id: int
    loan_count: int