import io
from decimal import Decimal
import pandas as pd
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Upload as UploadModel, PricingFeeds
from app.schemas.upload import UploadSummaryResponse
from fastapi import APIRouter, Depends, File, UploadFile

router = APIRouter()

@router.post("/upload", response_model=UploadSummaryResponse)
def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        return UploadSummaryResponse(
            accepted=0, 
            rejected=0, 
            total=0, 
            errors=["File must be a CSV"]
        )
    
    try:
        content = file.file.read().decode('utf-8')
        data = pd.read_csv(io.StringIO(content))
        
        expected_columns = {'Store ID', 'SKU', 'Product Name', 'Price', 'Date'}
        if not expected_columns.issubset(data.columns):
            missing = expected_columns - set(data.columns)
            return UploadSummaryResponse(
                accepted=0,
                rejected=0,
                total=0,
                errors=[f"Missing columns: {', '.join(missing)}"]
            )
        
        accepted = 0
        rejected = 0
        errors = []
        records = []
        
        for i, row in data.iterrows():
            row_num = i + 2
            
            # Extract and clean values
            fields = {
                'store_id': str(row['Store ID']).strip() if pd.notna(row['Store ID']) else '',
                'sku': str(row['SKU']).strip() if pd.notna(row['SKU']) else '',
                'product_name': str(row['Product Name']).strip() if pd.notna(row['Product Name']) else '',
                'price_str': str(row['Price']).strip() if pd.notna(row['Price']) else '',
                'date_str': str(row['Date']).strip() if pd.notna(row['Date']) else '',
            }
            
            # Validate required fields
            if not all(fields.values()):
                rejected += 1
                errors.append(f"Row {row_num}: Missing required fields")
                continue
            
            # Validate price
            try:
                price = Decimal(fields['price_str'])
                if price < 0:
                    raise ValueError("Price cannot be negative")
            except (ValueError, Exception) as e:
                rejected += 1
                errors.append(f"Row {row_num}: Invalid price - {str(e)}")
                continue
            
            # Validate date
            try:
                date_obj = pd.to_datetime(fields['date_str']).date()
            except (ValueError, Exception) as e:
                rejected += 1
                errors.append(f"Row {row_num}: Invalid date - {str(e)}")
                continue
            
            # Create record
            try:
                record = PricingFeeds(
                    store_id=fields['store_id'],
                    sku=fields['sku'],
                    product_name=fields['product_name'],
                    price=price,
                    date=date_obj,
                )
                records.append(record)
                accepted += 1
            except Exception as e:
                rejected += 1
                errors.append(f"Row {row_num}: {str(e)}")
        
        # Create upload record
        upload_record = UploadModel(
            filename=file.filename,
            file_path=f"/uploads/{file.filename}",
            row_count=accepted,
            error_count=rejected,
        )
        db.add(upload_record)
        db.flush()
        
        if records:
            db.add_all(records)
        db.commit()
        
        return UploadSummaryResponse(
            accepted=accepted,
            rejected=rejected,
            total=accepted + rejected,
            errors=errors,
            upload_id=upload_record.id
        )
        
    except Exception as e:
        db.rollback()
        return UploadSummaryResponse(
            accepted=0,
            rejected=0,
            total=0,
            errors=[f"Error processing file: {str(e)}"]
        )