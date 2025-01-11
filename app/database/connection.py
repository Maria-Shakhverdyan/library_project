from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
from app.config.settings import settings

# Базовый класс для моделей
Base = declarative_base()

# Создаём подключение к PostgreSQL для управления базами данных
database_admin_url = f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/postgres"
engine_admin = create_async_engine(database_admin_url, echo=True, isolation_level="AUTOCOMMIT")

# Создаём подключение к основной базе данных
database_url = f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
engine = create_async_engine(database_url, echo=True)

# Сессия для работы с основной базой данных
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_database_if_not_exists():
    """Создаёт базу данных, если она не существует."""
    async with engine_admin.connect() as conn:
        # Проверяем существование базы данных
        result = await conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{settings.db_name}'"))
        exists = result.scalar()
        if not exists:
            # Создаём базу данных
            await conn.execute(text(f"CREATE DATABASE {settings.db_name}"))
            print(f"База данных '{settings.db_name}' успешно создана.")
        else:
            print(f"База данных '{settings.db_name}' уже существует.")


async def get_db():
    """Получение сессии для работы с основной базой данных."""
    async with async_session() as session:
        yield session