from typing import Optional
from sqlalchemy.orm import Session
from backend.repositories.doctor_repository import DoctorRepository
from backend.models.doctor import Doctor

class DoctorService:
    def __init__(self):
        self.repository = DoctorRepository()

    def get_doctor_by_id(self, db: Session, doctor_id: int) -> Optional[Doctor]:
        """Retrieve a doctor's profile record by ID."""
        return self.repository.get(db, doctor_id)

    def update_doctor_profile(self, db: Session, doctor_id: int, full_name: Optional[str] = None, specialty: Optional[str] = None) -> Optional[Doctor]:
        """Update profile details of an authenticated doctor."""
        doctor = self.repository.get(db, doctor_id)
        if not doctor:
            return None
        
        update_data = {}
        if full_name is not None:
            update_data["full_name"] = full_name
        if specialty is not None:
            update_data["specialty"] = specialty
            
        if update_data:
            return self.repository.update(db, doctor, update_data)
        return doctor

# Instantiate global service singleton
doctor_service = DoctorService()
