import shutil
from typing import List
from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from sqlalchemy.orm import Session
import traceback

from backend.api.dependencies import get_current_doctor, get_db
from backend.models.doctor import Doctor
from backend.schemas.uploaded_document import UploadedDocumentResponse
from backend.services.rag_service import rag_service
from backend.services.consultation_service import consultation_service


from backend.api.dependencies import get_current_doctor, get_db
from backend.models.doctor import Doctor
from backend.schemas.uploaded_document import UploadedDocumentResponse
from backend.services.rag_service import rag_service
from backend.services.consultation_service import consultation_service

router = APIRouter(prefix="/api/consultations", tags=["Uploads"])

UPLOAD_DIR = Path("frontend/static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/{id}/upload", response_model=UploadedDocumentResponse)
def upload_consultation_document(
    id: int,
    request: Request,
    file: UploadFile = File(...),
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Upload a clinical report or image for a consultation and load it into the RAG engine."""
    # Verify that consultation exists and belongs to doctor
    consultation = consultation_service.get_consultation(db, consultation_id=id, doctor_id=current_doctor.id)
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found or unauthorized access."
        )
        
    try:
        # Create a unique path subdirectory per consultation to avoid filename collisions
        consultation_upload_dir = UPLOAD_DIR / str(id)
        consultation_upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = consultation_upload_dir / file.filename
        
        # Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        client_ip = request.client.host if request.client else None
        
        # Determine simple file extension
        suffix = Path(file.filename).suffix.lower().replace(".", "")
        if not suffix:
            suffix = "unknown"
            
        # Ingest file into database and RAG session pipeline
        doc = rag_service.upload_document(
            db,
            consultation_id=id,
            filename=file.filename,
            file_path=str(file_path.resolve()),
            file_type=suffix,
            doctor_id=current_doctor.id,
            ip_address=client_ip
        )
        
        return doc
    except Exception as e:
        print("\n" + "=" * 80)
        print("UPLOAD PIPELINE ERROR")
        traceback.print_exc()
        print("=" * 80)

        raise HTTPException(
        status_code=500,
        detail=f"Failed to process and index document: {e}"
    )

@router.get("/{id}/documents", response_model=List[UploadedDocumentResponse])
def get_consultation_documents(
    id: int,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Retrieve all files uploaded for this consultation."""
    consultation = consultation_service.get_consultation(db, consultation_id=id, doctor_id=current_doctor.id)
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found or unauthorized access."
        )
    return rag_service.get_uploaded_documents(db, consultation_id=id)
