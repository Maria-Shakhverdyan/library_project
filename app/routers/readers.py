from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.services.readers_service import get_readers, get_reader_by_id, create_reader, update_reader, delete_reader, deactivate_readers_without_loans
from app.schemas.readers import ReaderCreate, Reader

router = APIRouter()

@router.get("/", response_model=list[Reader])
async def read_readers(db: AsyncSession = Depends(get_db)):
    """Получение всех читателей."""
    return await get_readers(db)

@router.get("/{reader_id}", response_model=Reader)
async def read_reader(reader_id: int, db: AsyncSession = Depends(get_db)):
    """Получение читателя по ID."""
    reader = await get_reader_by_id(db, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader

@router.post("/", response_model=Reader)
async def add_reader(reader: ReaderCreate, db: AsyncSession = Depends(get_db)):
    """Добавление нового читателя."""
    return await create_reader(db, reader)

@router.put("/{reader_id}", response_model=Reader)
async def update_reader_endpoint(reader_id: int, reader: ReaderCreate, db: AsyncSession = Depends(get_db)):
    """Обновление читателя по ID."""
    updated_reader = await update_reader(db, reader_id, reader)
    if not updated_reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return updated_reader

@router.delete("/{reader_id}")
async def delete_reader_endpoint(reader_id: int, db: AsyncSession = Depends(get_db)):
    """Удаление читателя по ID."""
    if not await delete_reader(db, reader_id):
        raise HTTPException(status_code=404, detail="Reader not found")
    return {"message": "Reader deleted successfully"}

#UPDATE
@router.put("/deactivate-inactive")
async def deactivate_inactive_readers(db: AsyncSession = Depends(get_db)):
    count = await deactivate_readers_without_loans(db)
    return {"message": f"{count} readers deactivated."}