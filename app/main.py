import asyncio
from fastapi import FastAPI
from app.routers import books, readers, loans
from app.database.connection import create_database_if_not_exists, engine, Base

app = FastAPI()

# Подключение маршрутов
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(readers.router, prefix="/readers", tags=["Readers"])
app.include_router(loans.router, prefix="/loans", tags=["Loans"])

@app.on_event("startup")
async def on_startup():
    # Проверяем и создаём базу данных, если она отсутствует
    await create_database_if_not_exists()
    # Создаём таблицы, если их нет
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

