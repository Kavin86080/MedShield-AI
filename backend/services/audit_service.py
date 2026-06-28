from sqlalchemy.orm import Session
from backend.repositories.audit_log_repository import AuditLogRepository
from backend.models.audit_log import AuditLog

class AuditService:
    def __init__(self):
        self.repository = AuditLogRepository()

    def log_action(self, db: Session, doctor_id: int, action: str, ip_address: str = None) -> AuditLog:
        """Create a new audit log record."""
        log_entry = AuditLog(
            doctor_id=doctor_id,
            action=action,
            ip_address=ip_address
        )
        return self.repository.create(db, log_entry)

# Instantiate global service singleton
audit_service = AuditService()
