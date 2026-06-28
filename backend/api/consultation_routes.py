from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from backend.api.dependencies import get_current_doctor, get_db
from backend.models.doctor import Doctor
from backend.schemas.consultation import ConsultationCreateRequest, ConsultationCloseRequest, ConsultationResponse
from backend.services.consultation_service import consultation_service

router = APIRouter(prefix="/api/consultations", tags=["Consultations"])

@router.post("", response_model=ConsultationResponse)
def create_consultation(
    request: Request,
    payload: ConsultationCreateRequest,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Start a new patient consultation session."""
    client_ip = request.client.host if request.client else None
    return consultation_service.create_consultation(
        db,
        doctor_id=current_doctor.id,
        patient_name=payload.patient_name,
        patient_age=payload.patient_age,
        patient_gender=payload.patient_gender,
        ip_address=client_ip
    )

@router.get("", response_model=List[ConsultationResponse])
def list_consultations(
    skip: int = 0,
    limit: int = 100,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """List all consultation sessions managed by the logged-in doctor."""
    return consultation_service.list_consultations(db, doctor_id=current_doctor.id, skip=skip, limit=limit)

@router.get("/{id}", response_model=ConsultationResponse)
def get_consultation_details(
    id: int,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Fetch details of a specific consultation session."""
    consultation = consultation_service.get_consultation(db, consultation_id=id, doctor_id=current_doctor.id)
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found or unauthorized access."
        )
    return consultation

@router.post("/{id}/close", response_model=ConsultationResponse)
def close_consultation(
    id: int,
    request: Request,
    payload: ConsultationCloseRequest,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Mark a consultation session as completed and register the clinical summary."""
    client_ip = request.client.host if request.client else None
    updated = consultation_service.close_consultation(
        db,
        consultation_id=id,
        doctor_id=current_doctor.id,
        summary=payload.summary,
        ip_address=client_ip
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found or unauthorized access."
        )
    return updated

@router.delete("/{id}")
def delete_consultation(
    id: int,
    request: Request,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Delete a consultation session from records."""
    client_ip = request.client.host if request.client else None
    success = consultation_service.delete_consultation(
        db,
        consultation_id=id,
        doctor_id=current_doctor.id,
        ip_address=client_ip
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found or unauthorized access."
        )
    return {"status": "success", "message": "Consultation successfully deleted."}
