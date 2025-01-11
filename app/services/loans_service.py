from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from app.database.models.loans import Loan
from app.database.models.readers import Reader
from app.database.models.books import Book
from app.schemas.loans import LoanCreate, LoanGroupByBook, LoanDetail

async def get_loans(db: AsyncSession):
    """Получение всех выдач."""
    result = await db.execute(select(Loan))
    return result.scalars().all()

async def get_loan_by_id(db: AsyncSession, loan_id: int):
    """Получение выдачи по ID."""
    result = await db.execute(select(Loan).where(Loan.id == loan_id))
    return result.scalar()

async def create_loan(db: AsyncSession, loan: LoanCreate):
    """Создание новой выдачи."""
    new_loan = Loan(**loan.dict())
    db.add(new_loan)
    await db.commit()
    await db.refresh(new_loan)
    return new_loan

async def update_loan(db: AsyncSession, loan_id: int, loan: LoanCreate):
    """Обновление выдачи по ID."""
    existing_loan = await get_loan_by_id(db, loan_id)
    if not existing_loan:
        return None
    for key, value in loan.dict().items():
        setattr(existing_loan, key, value)
    await db.commit()
    await db.refresh(existing_loan)
    return existing_loan

async def delete_loan(db: AsyncSession, loan_id: int):
    """Удаление выдачи по ID."""
    existing_loan = await get_loan_by_id(db, loan_id)
    if not existing_loan:
        return False
    await db.delete(existing_loan)
    await db.commit()
    return True

#JOIN
async def get_detailed_loans_info(db: AsyncSession):
    result = await db.execute(
        select(
            Loan.id.label("loan_id"),
            Book.title.label("book_title"),
            Reader.name.label("reader_name")
        )
        .join(Book, Loan.book_id == Book.id)
        .join(Reader, Loan.reader_id == Reader.id)
    )
    return [
        LoanDetail(id=row.loan_id, book_title=row.book_title, reader_name=row.reader_name)
        for row in result.all()
    ]

#GROUP BY
async def count_active_loans_by_book(db: AsyncSession):
    result = await db.execute(
        select(Loan.book_id, func.count(Loan.id).label("loan_count"))
        .where(Loan.return_date == None)
        .group_by(Loan.book_id)
    )
    return [
        LoanGroupByBook(book_id=row.book_id, loan_count=row.loan_count)
        for row in result.all()
    ]