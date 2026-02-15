import os
import tempfile
from decimal import Decimal

import pandas as pd
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.db.models import Upload as UploadModel, PricingFeeds
from app.db.session import get_db
from app.schemas.upload import UploadSummaryResponse

router = APIRouter()

EXPECTED_COLUMNS = {"Store ID", "SKU", "Product Name", "Price", "Date"}


@router.post("/upload", response_model=UploadSummaryResponse)
def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        return UploadSummaryResponse(
            accepted=0, rejected=0, total=0, errors=["File must be a CSV"]
        )

    tmp_path = None
    try:
        # save uploaded file to temp so we can read it in chunks
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as f:
            tmp_path = f.name
            while True:
                data = file.file.read(1024 * 1024)
                if not data:
                    break
                f.write(data)

        # quick check that we have the right columns
        peek = pd.read_csv(tmp_path, nrows=0)
        if not EXPECTED_COLUMNS.issubset(peek.columns):
            missing = EXPECTED_COLUMNS - set(peek.columns)
            return UploadSummaryResponse(
                accepted=0,
                rejected=0,
                total=0,
                errors=[f"Missing columns: {', '.join(missing)}"],
            )

        upload_record = UploadModel(
            filename=file.filename,
            file_path=f"/uploads/{file.filename}",
            row_count=0,
            error_count=0,
        )
        db.add(upload_record)
        db.commit()
        db.refresh(upload_record)

        accepted = 0
        rejected = 0
        errors = []
        row_start = 0

        for chunk in pd.read_csv(tmp_path, chunksize=10000):
            records = []
            for idx, (_, row) in enumerate(chunk.iterrows()):
                row_num = row_start + idx + 2

                store_id = str(row["Store ID"]).strip() if pd.notna(row["Store ID"]) else ""
                sku = str(row["SKU"]).strip() if pd.notna(row["SKU"]) else ""
                product_name = str(row["Product Name"]).strip() if pd.notna(row["Product Name"]) else ""
                price_str = str(row["Price"]).strip() if pd.notna(row["Price"]) else ""
                date_str = str(row["Date"]).strip() if pd.notna(row["Date"]) else ""

                if not all([store_id, sku, product_name, price_str, date_str]):
                    rejected += 1
                    errors.append(f"Row {row_num}: Missing required fields")
                    continue

                try:
                    price = Decimal(price_str)
                    if price < 0:
                        raise ValueError("negative")
                except Exception as e:
                    rejected += 1
                    errors.append(f"Row {row_num}: Invalid price - {e}")
                    continue

                try:
                    date_obj = pd.to_datetime(date_str).date()
                except Exception as e:
                    rejected += 1
                    errors.append(f"Row {row_num}: Invalid date - {e}")
                    continue

                records.append(
                    PricingFeeds(
                        store_id=store_id,
                        sku=sku,
                        product_name=product_name,
                        price=price,
                        date=date_obj,
                    )
                )
                accepted += 1

            if records:
                db.add_all(records)
            db.commit()
            row_start += len(chunk)

        upload_record.row_count = accepted
        upload_record.error_count = rejected
        db.commit()

        return UploadSummaryResponse(
            accepted=accepted,
            rejected=rejected,
            total=accepted + rejected,
            errors=errors,
            upload_id=upload_record.id,
        )

    except Exception as e:
        db.rollback()
        return UploadSummaryResponse(
            accepted=0, rejected=0, total=0, errors=[str(e)]
        )
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
