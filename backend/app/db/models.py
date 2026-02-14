from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Numeric, Date, DateTime, Integer, Index

Base = declarative_base()

class Upload(Base):
    __tablename__ = 'uploads'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    row_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    error_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class PricingFeeds(Base):
    __tablename__ = 'pricing_feeds'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    sku: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    product_name: Mapped[str] = mapped_column(String(512), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    country_code: Mapped[str | None] = mapped_column(String(8), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index("index_pricing_feeds_store_sku_date", "store_id", "sku", "date"),
    )
