from pydantic import Field
from src.base_schemas import ExchangeRatesBase


class ExchangeRatesAPIResponse(ExchangeRatesBase):
    currency_iso_code: str = Field(alias="base")

    class Config:
        populate_by_name = True


class OpenExchangeRatesAPIResponse(ExchangeRatesBase):
    currency_iso_code: str = Field(alias="base")

    class Config:
        populate_by_name = True
