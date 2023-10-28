from pydantic import BaseModel
from typing import Dict


class ExchangeRatesBase(BaseModel):
    currency_iso_code: str
    rates: Dict[str, float]


class ExchangeServiceAPIResponse(ExchangeRatesBase):
    pass
