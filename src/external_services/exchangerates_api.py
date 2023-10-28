from src.external_services.abstract_exchange_api_service import AbstractExchangeApiService
from src.config import settings
from src.base_schemas import ExchangeServiceAPIResponse
from .response_schemas.schemas import ExchangeRatesAPIResponse
from src.utils import make_async_httpx_request


class ExchangeRatesApiService(AbstractExchangeApiService):
    @property
    def base_api_url(self) -> str:
        return "http://api.exchangeratesapi.io/v1/"

    @property
    def base_currency_iso_code(self) -> str:
        return "EUR"

    def _get_api_key(self) -> str:
        return settings.EXCHANGERATESAPI_API_KEY

    @property
    def _base_request_url(self) -> str:
        request_url = f"{self.base_api_url}latest?access_key={self._get_api_key()}"
        return request_url

    async def get_latest_rates(self) -> ExchangeServiceAPIResponse | None:
        api_data = await make_async_httpx_request(self._base_request_url)
        if api_data:
            parsed_data = ExchangeRatesAPIResponse(**api_data)
            rates = ExchangeServiceAPIResponse(**parsed_data.model_dump())
            return rates
        return
