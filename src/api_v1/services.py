import json
import pytz
from datetime import datetime
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, desc
from sqlalchemy.exc import DBAPIError
from src.external_services.abstract_exchange_api_service import AbstractExchangeApiService  # noqa E501
from src.base_schemas import ExchangeServiceAPIResponse
from src.utils import cache_currency_pair_rates, clear_pair_rates_cache
from .schemas import ExchangeRateCreate, ServiceResponses
from .db_models import ExchangeRates

service_response = ServiceResponses()


async def get_api_rates(
        exchangerates_service: AbstractExchangeApiService) -> ExchangeServiceAPIResponse:  # noqa E501
    new_rates = await exchangerates_service.get_latest_rates()
    return new_rates


async def create_rates(db_session: AsyncSession, rates: dict) -> None:
    new_rates = ExchangeRateCreate(**rates)
    db_session.add(ExchangeRates(**new_rates.model_dump()))
    await db_session.commit()


@clear_pair_rates_cache
async def update_rates(db_session: AsyncSession,
                       exchangerates_service: AbstractExchangeApiService) -> json:  # noqa E501
    new_rates = await get_api_rates(exchangerates_service=exchangerates_service)
    if not new_rates:
        raise HTTPException(status_code=500,
                            detail=service_response.SERVER_ERROR)
    try:
        update_stmt = (
            update(ExchangeRates).
            where(ExchangeRates.currency_iso_code == exchangerates_service.base_currency_iso_code).  # noqa E501
            values(rates=new_rates.rates))

        update_result = await db_session.execute(update_stmt)
        await db_session.commit()
        if update_result.rowcount == 0:
            await create_rates(db_session=db_session,
                               rates=new_rates.model_dump())
        return service_response.RATES_UPDATED
    except DBAPIError as e:  # noqa F841
        raise HTTPException(status_code=500,
                            detail=service_response.SERVER_ERROR)


async def get_latest_rates(db_session: AsyncSession) -> ExchangeRates | None:
    query_stmt = select(ExchangeRates).order_by(desc(ExchangeRates.updated_at))
    query_result = await db_session.execute(query_stmt)
    return query_result.scalars().first()


async def _convert_date_in_moscow_tz(date: datetime) -> datetime:
    return date.astimezone(pytz.timezone('Europe/Moscow'))


async def fetch_last_update(db_session: AsyncSession):
    try:
        latest_rates = await get_latest_rates(db_session=db_session)
        last_update = await _convert_date_in_moscow_tz(latest_rates.updated_at)
        return service_response.last_update_response(last_update)
    except DBAPIError as e:  # noqa F841
        raise HTTPException(
            status_code=500, detail=service_response.SERVER_ERROR)


async def _get_currency_rate(
        latest_rates: ExchangeRates, currency_iso_code: str) -> float:
    if currency_iso_code == latest_rates.currency_iso_code:
        return 1
    else:
        return latest_rates.rates.get(currency_iso_code)


@cache_currency_pair_rates
async def get_pair_rate(
        db_session: AsyncSession, from_base: str, to_target: str):
    latest_rates = await get_latest_rates(db_session=db_session)
    base_currency_rate = await _get_currency_rate(latest_rates=latest_rates,
                                                  currency_iso_code=from_base)
    target_currency_rate = await _get_currency_rate(latest_rates=latest_rates,
                                                    currency_iso_code=to_target)
    return target_currency_rate / base_currency_rate


async def make_conversion(
        db_session: AsyncSession,
        amount: float, from_base: str, to_target: str):
    pair_rate = await get_pair_rate(db_session=db_session,
                                    from_base=from_base,
                                    to_target=to_target)
    return pair_rate * amount
