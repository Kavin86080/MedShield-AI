from typing import List
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.models.consultation import Consultation

class ConsultationRepository(BaseRepository[Consultation]):
    def __init__(self):
        super().__init__(Consultation)

    def get_by_doctor(self, db: Session, doctor_id: int, skip: int = 0, limit: int = 100) -> List[Consultation]:
        """Fetch all consultations created by a specific doctor."""
        return db.query(Consultation).filter(Consultation.doctor_id == doctor_id).order_by(Consultation.created_at.desc()).offset(skip).limit(limit).all()
