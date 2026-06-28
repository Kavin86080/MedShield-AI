from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class ConsultationCreateRequest(BaseModel):
    patient_name: str
    patient_age: int
    patient_gender: str

class ConsultationCloseRequest(BaseModel):
    summary: Optional[str] = None

class ConsultationResponse(BaseModel):
    id: int
    doctor_id: int
    patient_name: str
    patient_age: int
    patient_gender: str
    status: str
    summary: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
