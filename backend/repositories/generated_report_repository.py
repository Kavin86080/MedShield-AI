from typing import List
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.models.generated_report import GeneratedReport

class GeneratedReportRepository(BaseRepository[GeneratedReport]):
    def __init__(self):
        super().__init__(GeneratedReport)

    def get_by_consultation(self, db: Session, consultation_id: int) -> List[GeneratedReport]:
        """Fetch all clinical reports generated for a specific consultation session."""
        return db.query(GeneratedReport).filter(GeneratedReport.consultation_id == consultation_id).order_by(GeneratedReport.created_at.desc()).all()
