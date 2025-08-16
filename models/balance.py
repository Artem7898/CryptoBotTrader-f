from sqlalchemy import String, Float, BigInteger, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .base import Base


class Balance(Base):
    __tablename__ = "balances"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    asset:  Mapped[str] = mapped_column(String(16), index=True)  # USDT, BTC ...
    free:   Mapped[float] = mapped_column(Float)
    ts:     Mapped[datetime] = mapped_column(DateTime)
    __table_args__ = (Index("ix_balances_asset_ts", "asset","ts"),)
