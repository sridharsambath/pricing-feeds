from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class ProductSchema(BaseModel):
    id: int
    store_id: str
    sku: str
    product_name: str
    price: float
    date: date
    country_code: str | None = None
    
    class Config:
        from_attributes = True

class ProductUpdateSchema(BaseModel):
    store_id: Optional[str] = None
    sku: Optional[str] = None
    product_name: Optional[str] = None
    price: Optional[float] = None
    date: Optional[date] = None
    country_code: Optional[str] = None
    
    class Config:
        extra = 'forbid'

class PaginationMetadata(BaseModel):
    page: int
    limit: int
    total: int
    has_more: bool

class ProductResponse(BaseModel):
    data: List[ProductSchema]
    pagination: PaginationMetadata