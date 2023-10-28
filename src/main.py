from fastapi import FastAPI
from .config import app_configs, settings
from .api_v1.router import router as api_router
from .base_dependencies import get_exchangerates_service
from src.api_v1.services import update_rates
from .database.database import session_factory
from redis import asyncio as aioredis
from src import redis
from contextlib import asynccontextmanager
from typing import AsyncGenerator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # Startup
    pool = aioredis.ConnectionPool.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        max_connections=10, decode_responses=True)
    redis.redis_client = aioredis.Redis(connection_pool=pool)

    # Updating rates. If no data in database here it fill first.
    async with session_factory() as session:
        exchangerates_service = await get_exchangerates_service()
        await update_rates(session, exchangerates_service)
    yield
    # Shutdown
    await pool.disconnect()


app = FastAPI(**app_configs, lifespan=lifespan)
api_prefix = settings.API_V1_STR
app.include_router(api_router, prefix=api_prefix)
