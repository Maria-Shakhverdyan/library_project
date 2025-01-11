from pydantic import BaseModel
from typing import Optional

class ReaderBase(BaseModel):
    """Базовая схема для читателя."""
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    passport_number: Optional[str] = None
    is_active: Optional[bool] = True

class ReaderCreate(ReaderBase):
    """Схема для создания читателя."""
    pass

class Reader(ReaderBase):
    """Схема для представления читателя."""
    id: int

    class Config:
        orm_mode = True