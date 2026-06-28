from typing import List
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.models.audit_log import AuditLog

class AuditLogRepository(BaseRepository[AuditLog]):
    def __init__(self):
        super().__init__(AuditLog)

    def get_by_doctor(self, db: Session, doctor_id: int, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Fetch audit log history for a specific doctor."""
        return db.query(AuditLog).filter(AuditLog.doctor_id == doctor_id).order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
