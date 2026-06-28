from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.api.dependencies import get_current_doctor, get_db
from backend.models.doctor import Doctor
from backend.schemas.doctor import DoctorProfileResponse, DoctorUpdateRequest
from backend.schemas.audit_log import AuditLogResponse
from backend.services.doctor_service import doctor_service
from backend.repositories.audit_log_repository import AuditLogRepository

router = APIRouter(prefix="/api/doctors", tags=["Doctors"])
audit_repo = AuditLogRepository()

@router.get("/me", response_model=DoctorProfileResponse)
def get_current_doctor_profile(current_doctor: Doctor = Depends(get_current_doctor)):
    """Retrieve details of the currently logged-in doctor."""
    return current_doctor

@router.put("/me", response_model=DoctorProfileResponse)
def update_doctor_profile(
    payload: DoctorUpdateRequest,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Update profile information for the currently logged-in doctor."""
    updated = doctor_service.update_doctor_profile(
        db,
        doctor_id=current_doctor.id,
        full_name=payload.full_name,
        specialty=payload.specialty
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failed to update doctor profile."
        )
    return updated

@router.get("/me/audit-logs", response_model=List[AuditLogResponse])
def get_my_audit_logs(
    skip: int = 0,
    limit: int = 50,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Fetch security audit logs for the logged-in doctor."""
    logs = audit_repo.get_by_doctor(db, doctor_id=current_doctor.id, skip=skip, limit=limit)
    return logs
