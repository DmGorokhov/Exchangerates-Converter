from fastapi import APIRouter, Depends, status
from src.base_dependencies import get_db_session, get_exchangerates_service
from sqlalchemy.ext.asyncio import AsyncSession
from src.external_services.abstract_exchange_api_service import AbstractExchangeApiService
from .services import update_rates, fetch_last_update, make_conversion
from .dependencies import get_currency_codes
from typing import Annotated

router = APIRouter(responses={404: {"description": "Not found"}})


@router.get("/convert", status_code=status.HTTP_200_OK)
async def get_conversion(amount: float,
                         currency_codes: Annotated[dict, Depends(get_currency_codes)],
                         session: AsyncSession = Depends(get_db_session)):
    convert_response = await make_conversion(db_session=session,
                                             amount=amount,
                                             **currency_codes)
    return convert_response


@router.get("/update_rates", status_code=status.HTTP_200_OK)
async def make_update_rates(
        session: AsyncSession = Depends(get_db_session),
        exchangerates_service: AbstractExchangeApiService = Depends(
            get_exchangerates_service)):
    update_response = await update_rates(
        db_session=session, exchangerates_service=exchangerates_service)
    return update_response


@router.get("/last_update", status_code=status.HTTP_200_OK)
async def get_last_update(session: AsyncSession = Depends(get_db_session)):
    last_update_response = await fetch_last_update(db_session=session)
    return last_update_response
