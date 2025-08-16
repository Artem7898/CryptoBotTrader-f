from sqlalchemy import String, Float, BigInteger, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .base import Base


class Position(Base):
    __tablename__ = "positions"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    symbol:  Mapped[str] = mapped_column(String(32), index=True)
    qty:     Mapped[float] = mapped_column(Float, default=0.0)
    ts:      Mapped[datetime] = mapped_column(DateTime)
    __table_args__ = (Index("ix_positions_symbol_ts", "symbol","ts"),)
