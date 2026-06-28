from typing import List, Optional
from sqlalchemy.orm import Session
from backend.repositories.consultation_repository import ConsultationRepository
from backend.models.consultation import Consultation
from backend.services.audit_service import audit_service

class ConsultationService:
    def __init__(self):
        self.repository = ConsultationRepository()

    def create_consultation(self, db: Session, doctor_id: int, patient_name: str, patient_age: int, patient_gender: str, ip_address: Optional[str] = None) -> Consultation:
        """Create a new consultation session and record in audit log."""
        new_consultation = Consultation(
            doctor_id=doctor_id,
            patient_name=patient_name,
            patient_age=patient_age,
            patient_gender=patient_gender,
            status="active"
        )
        created = self.repository.create(db, new_consultation)
        
        # Log action
        audit_service.log_action(db, doctor_id, f"create_consultation: {created.id}", ip_address)
        return created

    def get_consultation(self, db: Session, consultation_id: int, doctor_id: int) -> Optional[Consultation]:
        """Fetch details of a consultation. Verifies that it belongs to the requesting doctor."""
        consultation = self.repository.get(db, consultation_id)
        if consultation and consultation.doctor_id == doctor_id:
            return consultation
        return None

    def list_consultations(self, db: Session, doctor_id: int, skip: int = 0, limit: int = 100) -> List[Consultation]:
        """List consultations for a specific doctor in descending order."""
        return self.repository.get_by_doctor(db, doctor_id, skip, limit)

    def close_consultation(self, db: Session, consultation_id: int, doctor_id: int, summary: Optional[str] = None, ip_address: Optional[str] = None) -> Optional[Consultation]:
        """Mark a consultation session as completed and save final clinical summary."""
        consultation = self.get_consultation(db, consultation_id, doctor_id)
        if not consultation:
            return None
        
        update_data = {"status": "completed"}
        if summary:
            update_data["summary"] = summary
            
        updated = self.repository.update(db, consultation, update_data)
        
        # Log action
        audit_service.log_action(db, doctor_id, f"close_consultation: {consultation_id}", ip_address)
        return updated

    def delete_consultation(self, db: Session, consultation_id: int, doctor_id: int, ip_address: Optional[str] = None) -> bool:
        """Delete a consultation session."""
        consultation = self.get_consultation(db, consultation_id, doctor_id)
        if not consultation:
            return False
            
        success = self.repository.delete(db, consultation_id)
        if success:
            audit_service.log_action(db, doctor_id, f"delete_consultation: {consultation_id}", ip_address)
        return success

# Instantiate global service singleton
consultation_service = ConsultationService()
