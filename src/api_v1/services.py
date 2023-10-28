import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, desc
from sqlalchemy.exc import DBAPIError
from .db_models import ExchangeRates
from src.external_services.abstract_exchange_api_service import AbstractExchangeApiService
from src.base_schemas import ExchangeServiceAPIResponse
from .schemas import ExchangeRateCreate, ServiceResponses
from fastapi.exceptions import HTTPException

service_response = ServiceResponses()


async def get_api_rates(
        exchangerates_service: AbstractExchangeApiService) -> ExchangeServiceAPIResponse:
    new_rates = await exchangerates_service.get_latest_rates()
    return new_rates


async def create_rates(db_session: AsyncSession, rates: dict) -> None:
    new_rates = ExchangeRateCreate(**rates)
    db_session.add(ExchangeRates(**new_rates.model_dump()))
    await db_session.commit()


async def update_rates(db_session: AsyncSession,
                       exchangerates_service: AbstractExchangeApiService) -> json:
    new_rates = await get_api_rates(exchangerates_service=exchangerates_service)
    if not new_rates:
        raise HTTPException(status_code=500,
                            detail=service_response.SERVER_ERROR)
    try:
        update_stmt = (update(ExchangeRates).
                       where(ExchangeRates.currency_iso_code == exchangerates_service.base_currency_iso_code).
                       values(rates=new_rates.rates))

        update_result = await db_session.execute(update_stmt)
        await db_session.commit()
        if update_result.rowcount == 0:
            await create_rates(db_session=db_session, rates=new_rates.model_dump())
        return service_response.RATES_UPDATED
    except DBAPIError as e:
        raise HTTPException(status_code=500,
                            detail=service_response.SERVER_ERROR)


async def get_latest_rates(db_session: AsyncSession) -> ExchangeRates | None:
    query_stmt = select(ExchangeRates).order_by(desc(ExchangeRates.updated_at))
    query_result = await db_session.execute(query_stmt)
    return query_result.scalars().first()


async def fetch_last_update(db_session: AsyncSession):
    try:
        latest_rates = await get_latest_rates(db_session=db_session)
        return service_response.last_update_response(latest_rates.updated_at)
    except DBAPIError as e:
        raise HTTPException(
            status_code=500, detail=service_response.SERVER_ERROR)


async def _get_currency_rate(latest_rates: ExchangeRates, currency_iso_code: str) -> float:
    if currency_iso_code == latest_rates.currency_iso_code:
        return 1
    else:
        return latest_rates.rates.get(currency_iso_code)


async def get_pair_rate(base_currency: str, target_currency: str, latest_rates: ExchangeRates) -> float:
    base_currency_rate = await _get_currency_rate(latest_rates=latest_rates, currency_iso_code=base_currency)
    target_currency_rate = await _get_currency_rate(latest_rates=latest_rates, currency_iso_code=target_currency)
    return target_currency_rate / base_currency_rate


async def make_conversion(
        db_session: AsyncSession, amount: float, from_base: str, to_target: str):
    latest_rates = await get_latest_rates(db_session=db_session)
    pair_rate = await get_pair_rate(from_base, to_target, latest_rates)
    return pair_rate * amount
