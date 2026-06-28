from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class DoctorProfileResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    specialty: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class DoctorUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    specialty: Optional[str] = None
