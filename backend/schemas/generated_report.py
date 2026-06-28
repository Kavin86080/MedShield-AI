from datetime import datetime
from pydantic import BaseModel

class ReportGenerateRequest(BaseModel):
    report_type: str = "clinical_summary"  # clinical_summary, imaging_report, etc.

class GeneratedReportResponse(BaseModel):
    id: int
    consultation_id: int
    content: str
    report_type: str
    created_at: datetime

    class Config:
        from_attributes = True
