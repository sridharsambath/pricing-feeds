from sqlalchemy import Column, Integer, String, create_engine, DateTime, Float, Index
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Upload(Base):
    __tablename__ = 'uploads'
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    row_count = Column(Integer, nullable=True)
    error_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True)
    uploaded_at = Column(DateTime, nullable=True)

class PricingFeeds(Base):
    __tablename__ = 'pricing_feeds'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    store_id = Column(String(150), nullable=False)
    sku = Column(String(64), nullable=False)
    product_name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    country_code = Column(String(2), nullable=True)

Index("ix_pricing_feeds_store_id", PricingFeeds.store_id)
Index("ix_pricing_feeds_sku", PricingFeeds.sku)
Index("ix_pricing_feeds_date", PricingFeeds.date)
Index("ix_pricing_feeds_country_code", PricingFeeds.country_code)
Index("ix_pricing_feeds_store_sku_date", PricingFeeds.store_id, PricingFeeds.sku, PricingFeeds.date)


SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin123@localhost:5433/pricing_feeds"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
