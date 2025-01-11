from sqlalchemy import Column, Integer, String, Boolean
from app.database.connection import Base

class Reader(Base):
    __tablename__ = "readers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    passport_number = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    description = Column(String, nullable=True)  # Новое поле