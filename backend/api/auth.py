from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from backend.database.session import get_db
from backend.services.auth_service import auth_service
from backend.api.dependencies import get_current_doctor
from backend.models.doctor import Doctor
from backend.schemas.auth import DoctorRegisterRequest, DoctorLoginRequest, TokenResponse

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
def register(request: Request, payload: DoctorRegisterRequest, db: Session = Depends(get_db)):
    """Register a new doctor account and immediately issue JWT tokens."""
    client_ip = request.client.host if request.client else None
    doctor, error = auth_service.register_doctor(
        db,
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
        specialty=payload.specialty,
        ip_address=client_ip
    )
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    # Issue tokens upon successful registration
    access_token = auth_service.create_access_token(data={"sub": str(doctor.id)})
    refresh_token = auth_service.create_refresh_token(data={"sub": str(doctor.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=TokenResponse)
def login(request: Request, payload: DoctorLoginRequest, db: Session = Depends(get_db)):
    """Authenticate doctor credentials and issue Access and Refresh JWT tokens."""
    client_ip = request.client.host if request.client else None
    doctor, error = auth_service.authenticate_doctor(
        db,
        email=payload.email,
        password=payload.password,
        ip_address=client_ip
    )
    if error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error
        )
        
    access_token = auth_service.create_access_token(data={"sub": str(doctor.id)})
    refresh_token = auth_service.create_refresh_token(data={"sub": str(doctor.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: Request, refresh_token: str, db: Session = Depends(get_db)):
    """Validate a Refresh Token and issue a new Access Token."""
    payload = auth_service.verify_token(refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token."
        )
        
    doctor_id = payload.get("sub")
    if not doctor_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload."
        )
        
    access_token = auth_service.create_access_token(data={"sub": str(doctor_id)})
    new_refresh_token = auth_service.create_refresh_token(data={"sub": str(doctor_id)})
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


class DoctorProfileResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    specialty: Optional[str] = None

    class Config:
        from_attributes = True


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


@router.get("/me", response_model=DoctorProfileResponse)
def get_current_doctor_profile(
    current_doctor: Doctor = Depends(get_current_doctor)
):
    """Return the authenticated doctor's profile information."""
    return current_doctor


@router.post("/change-password")
def change_password(
    payload: ChangePasswordRequest,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Change the authenticated doctor's password after verifying current credentials."""
    if not auth_service.verify_password(payload.current_password, current_doctor.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect."
        )
    if len(payload.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 8 characters."
        )
    new_hash = auth_service.get_password_hash(payload.new_password)
    current_doctor.password_hash = new_hash
    db.commit()
    return {"message": "Password updated successfully."}
