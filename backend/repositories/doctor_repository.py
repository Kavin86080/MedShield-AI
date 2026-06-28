from typing import Optional
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.models.doctor import Doctor

class DoctorRepository(BaseRepository[Doctor]):
    def __init__(self):
        super().__init__(Doctor)

    def get_by_email(self, db: Session, email: str) -> Optional[Doctor]:
        """Fetch a doctor record by email."""
        return db.query(Doctor).filter(Doctor.email == email).first()
