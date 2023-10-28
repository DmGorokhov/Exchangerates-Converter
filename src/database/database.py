from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config import settings

DATABASE_URL = settings.pgdb_url

async_engine = create_async_engine(DATABASE_URL)
session_factory = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
