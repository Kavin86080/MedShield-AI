from datetime import datetime
from pydantic import BaseModel

class UploadedDocumentResponse(BaseModel):
    id: int
    consultation_id: int
    filename: str
    file_path: str
    file_type: str
    created_at: datetime

    class Config:
        from_attributes = True
