from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
from app.config.settings import settings

# Base class for models
Base = declarative_base()

# Connection URL for PostgreSQL database management
database_admin_url = f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/postgres"
engine_admin = create_async_engine(database_admin_url, echo=True, isolation_level="AUTOCOMMIT")

# Connection URL for the primary database
database_url = f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
engine = create_async_engine(database_url, echo=True)

# Session for working with the primary database
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def create_database_if_not_exists():
    """
    Create the database if it does not already exist.
    """
    async with engine_admin.connect() as conn:
        # Check if the database exists
        result = await conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{settings.db_name}'"))
        exists = result.scalar()
        if not exists:
            # Create the database
            await conn.execute(text(f"CREATE DATABASE {settings.db_name}"))
            print(f"Database '{settings.db_name}' successfully created.")
        else:
            print(f"Database '{settings.db_name}' already exists.")

async def get_db():
    """
    Get a session for working with the primary database.
    """
    async with async_session() as session:
        yield session
