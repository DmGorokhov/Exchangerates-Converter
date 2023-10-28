from src.external_services.abstract_exchange_api_service import AbstractExchangeApiService
from src.config import settings
from src.base_schemas import ExchangeServiceAPIResponse
from .response_schemas.schemas import OpenExchangeRatesAPIResponse
from src.utils import make_async_httpx_request


class OpenExchangeRatesApiService(AbstractExchangeApiService):
    @property
    def base_api_url(self) -> str:
        return "https://openexchangerates.org/api/"

    @property
    def base_currency_iso_code(self) -> str:
        return "USD"

    def _get_api_key(self) -> str:
        return settings.OPENEXCHANGERATES_API_KEY

    @property
    def _base_request_url(self) -> str:
        request_url = f"{self.base_api_url}latest.json?app_id={self._get_api_key()}"
        return request_url

    async def get_latest_rates(self) -> ExchangeServiceAPIResponse | None:
        api_data = await make_async_httpx_request(self._base_request_url)
        if api_data:
            parsed_data = OpenExchangeRatesAPIResponse(**api_data)
            rates = ExchangeServiceAPIResponse(**parsed_data.model_dump())
            return rates
        return
