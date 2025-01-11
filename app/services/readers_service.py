from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update

from app.database.models.readers import Reader
from app.database.models.loans import Loan
from app.schemas.readers import ReaderCreate


async def get_readers(db: AsyncSession):
    """
    Retrieve all readers.
    """
    result = await db.execute(select(Reader))
    return result.scalars().all()


async def get_reader_by_id(db: AsyncSession, reader_id: int):
    """
    Retrieve a reader by their ID.
    """
    result = await db.execute(select(Reader).where(Reader.id == reader_id))
    return result.scalar()


async def create_reader(db: AsyncSession, reader: ReaderCreate):
    """
    Create a new reader.
    """
    new_reader = Reader(**reader.dict())
    db.add(new_reader)
    await db.commit()
    await db.refresh(new_reader)
    return new_reader


async def update_reader(db: AsyncSession, reader_id: int, reader: ReaderCreate):
    """
    Update a reader by their ID.
    """
    existing_reader = await get_reader_by_id(db, reader_id)
    if not existing_reader:
        return None
    for key, value in reader.dict().items():
        setattr(existing_reader, key, value)
    await db.commit()
    await db.refresh(existing_reader)
    return existing_reader


async def delete_reader(db: AsyncSession, reader_id: int):
    """
    Delete a reader by their ID.
    """
    existing_reader = await get_reader_by_id(db, reader_id)
    if not existing_reader:
        return False
    await db.delete(existing_reader)
    await db.commit()
    return True


async def deactivate_readers_without_loans(db: AsyncSession):
    """
    Deactivate readers without active loans.
    """
    result = await db.execute(
        update(Reader)
        .where(~Reader.loans.any(Loan.return_date == None))  # No active loans
        .values(is_active=False)
        .execution_options(synchronize_session="fetch")
    )
    await db.commit()
    return result.rowcount
