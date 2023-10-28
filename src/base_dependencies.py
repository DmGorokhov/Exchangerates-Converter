from sqlalchemy.ext.asyncio import AsyncSession
from .database.database import session_factory
from src.external_services.exchangerates_api import ExchangeRatesApiService
from src.external_services.openexchangerates_api import OpenExchangeRatesApiService
from src.external_services.abstract_exchange_api_service import AbstractExchangeApiService
from src.config import settings

EXCHANGE_RATE_SERVICES = {
    "openexchangerates": OpenExchangeRatesApiService,
    "exchangerates": ExchangeRatesApiService,
}


async def get_db_session() -> AsyncSession:
    async with session_factory() as session:
        yield session
        await session.close()


async def get_exchangerates_service() -> AbstractExchangeApiService:
    service_name = settings.EXCHANGERATE_API_SERVICE
    api_client = EXCHANGE_RATE_SERVICES.get(service_name)()
    return api_client

