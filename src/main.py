from fastapi import FastAPI
from .config import app_configs, settings
from .api_v1.router import router as api_router
from .base_dependencies import get_exchangerates_service
from src.api_v1.services import update_rates
from .database.database import session_factory

app = FastAPI(**app_configs)


@app.on_event("startup")
async def refresh_exchange_rates():
    async with session_factory() as session:
        exchangerates_service = await get_exchangerates_service()
        await update_rates(session, exchangerates_service)


api_prefix = settings.API_V1_STR
app.include_router(api_router, prefix=api_prefix)
