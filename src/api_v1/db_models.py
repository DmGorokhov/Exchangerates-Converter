from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, JSON
from datetime import datetime
from sqlalchemy.sql.sqltypes import DateTime
from src.database.base import Base


class ExchangeRates(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    currency_name: Mapped[str]
    currency_iso_code: Mapped[str] = mapped_column(unique=True)
    rates: Mapped[dict] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
