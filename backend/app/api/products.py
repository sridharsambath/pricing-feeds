from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import PricingFeeds
from app.schemas.products import ProductResponse, ProductSchema, ProductUpdateSchema
from datetime import date
from typing import Optional

router = APIRouter()

@router.get("/products", response_model=ProductResponse)
def get_products_with_search_and_pagination(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    store_id: Optional[str] = Query(None, description="Filter by store ID"),
    sku: Optional[str] = Query(None, description="Filter by SKU"),
    product_name: Optional[str] = Query(None, description="Filter by product name (partial match)"),
    date_from: Optional[date] = Query(None, description="Filter by start date"),
    date_to: Optional[date] = Query(None, description="Filter by end date"),
    country_code: Optional[str] = Query(None, description="Filter by country code"),
):
    try:
        query = db.query(PricingFeeds)
        
        if store_id:
            query = query.filter(PricingFeeds.store_id == store_id)
        if sku:
            query = query.filter(PricingFeeds.sku == sku)
        if product_name:
            query = query.filter(PricingFeeds.product_name.ilike(f"%{product_name}%"))
        if date_from:
            query = query.filter(PricingFeeds.date >= date_from)
        if date_to:
            query = query.filter(PricingFeeds.date <= date_to)
        if country_code:
            query = query.filter(PricingFeeds.country_code == country_code)
        
        total = query.count()
        query = query.order_by(PricingFeeds.id.asc())
        skip = (page - 1) * limit
        products = query.offset(skip).limit(limit).all()
        
        return {
            "data": products,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "has_more": (page * limit) < total
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/products/{product_id}", response_model=ProductSchema)
def update_product(
    product_id: int,
    product_update: ProductUpdateSchema,
    db: Session = Depends(get_db),
):
    try:
        product = db.query(PricingFeeds).filter(PricingFeeds.id == product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        update_data = product_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        db.commit()
        db.refresh(product)
        
        return product
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))