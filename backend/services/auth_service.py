import os
from datetime import datetime, timedelta
from typing import Optional, Tuple
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from backend.repositories.doctor_repository import DoctorRepository
from backend.models.doctor import Doctor
from backend.services.audit_service import audit_service

# Load configuration from environment
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey123changethis")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.doctor_repo = DoctorRepository()

    def get_password_hash(self, password: str) -> str:
        """Hash a plaintext password using bcrypt."""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify that a plaintext password matches its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Generate a short-lived JWT Access Token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Generate a long-lived JWT Refresh Token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_token(self, token: str, token_type: str = "access") -> Optional[dict]:
        """Decode and verify JWT token validity and type."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != token_type:
                return None
            return payload
        except JWTError:
            return None

    def register_doctor(self, db: Session, email: str, password: str, full_name: str, specialty: Optional[str] = None, ip_address: Optional[str] = None) -> Tuple[Optional[Doctor], Optional[str]]:
        """Register a new Doctor."""
        existing = self.doctor_repo.get_by_email(db, email)
        if existing:
            return None, "Email address is already registered."
        
        hashed_password = self.get_password_hash(password)
        new_doctor = Doctor(
            email=email,
            password_hash=hashed_password,
            full_name=full_name,
            specialty=specialty
        )
        created_doctor = self.doctor_repo.create(db, new_doctor)
        
        # Log audit log
        audit_service.log_action(db, created_doctor.id, "doctor_register", ip_address)
        
        return created_doctor, None

    def authenticate_doctor(self, db: Session, email: str, password: str, ip_address: Optional[str] = None) -> Tuple[Optional[Doctor], Optional[str]]:
        """Authenticate a doctor and return the model instance."""
        doctor = self.doctor_repo.get_by_email(db, email)
        if not doctor:
            # Log failed login attempt
            audit_service.log_action(db, None, f"failed_login_attempt: {email}", ip_address)
            return None, "Invalid clinical email or password."
        
        if not self.verify_password(password, doctor.password_hash):
            audit_service.log_action(db, doctor.id, "failed_password_attempt", ip_address)
            return None, "Invalid clinical email or password."
        
        # Log successful login
        audit_service.log_action(db, doctor.id, "doctor_login", ip_address)
        return doctor, None

# Instantiate global service singleton
auth_service = AuthService()
