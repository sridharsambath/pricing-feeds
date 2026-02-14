from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class UploadSummaryResponse(BaseModel):
    accepted: int
    rejected: int
    total: int
    errors: list[str] = []
    upload_id: Optional[int] = None
