from typing import List
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.models.uploaded_document import UploadedDocument

class UploadedDocumentRepository(BaseRepository[UploadedDocument]):
    def __init__(self):
        super().__init__(UploadedDocument)

    def get_by_consultation(self, db: Session, consultation_id: int) -> List[UploadedDocument]:
        """Fetch all documents uploaded for a specific consultation."""
        return db.query(UploadedDocument).filter(UploadedDocument.consultation_id == consultation_id).all()
