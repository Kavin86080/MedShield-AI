from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class AuditLogResponse(BaseModel):
    id: int
    doctor_id: Optional[int]
    action: str
    ip_address: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
