from pydantic_settings import BaseSettings
from .constants import Environment
from typing import Optional, Any
from pydantic import EmailStr


class Settings(BaseSettings):
    API_VERSION: str = "v1"
    API_V1_STR: str = f"/api/{API_VERSION}"
    DB_ENGINE: str
    DB_HOST: str
    DB_PORT: int | str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    PGADMIN_MAIL: Optional[EmailStr]
    PGADMIN_PW: Optional[str]
    PROJECT_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    EXCHANGERATE_API_SERVICE: str
    EXCHANGERATESAPI_API_KEY: str = ""
    OPENEXCHANGERATES_API_KEY: str = ""

    @property
    def pgdb_url(self):
        return (f'{self.DB_ENGINE}://'
                f'{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')  # noqa E501

    class Config:
        env_file = ".env"


settings = Settings()

app_configs: dict[str, Any] = {
    "title": settings.PROJECT_NAME,
    "openapi_url": f"{settings.API_V1_STR}/openapi.json"}

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
