from abc import ABC, abstractmethod
from src.base_schemas import ExchangeServiceAPIResponse


class AbstractExchangeApiService(ABC):
    @property
    @abstractmethod
    def base_api_url(self) -> str:
        pass

    @property
    @abstractmethod
    def base_currency_iso_code(self) -> str:
        pass

    @abstractmethod
    def _get_api_key(self) -> str:
        pass

    @property
    @abstractmethod
    def _base_request_url(self) -> str:
        pass

    @abstractmethod
    async def get_latest_rates(self) -> ExchangeServiceAPIResponse:
        pass
