from pydantic import BaseModel, model_validator
from datetime import datetime
from src.base_schemas import ExchangeRatesBase
import pycountry


class ExchangeRateCreate(ExchangeRatesBase):
    currency_name: str

    @model_validator(mode="before")
    def fetch_currency_name(cls, values):
        currency = pycountry.currencies.get(
            alpha_3=values.get("currency_iso_code")
        )
        if currency:
            values['currency_name'] = currency.name
        return values


class ServiceResponses(BaseModel):
    RATES_UPDATED: dict = {"success": "Rates were successfully updated"}
    SERVER_ERROR: dict = {"error": "Sorry, service is unavailable now"}

    def last_update_response(self, last_updated_time: datetime):
        return {
            "The latest update was":
                last_updated_time.strftime("%Y-%m-%d %H:%M:%S")}
