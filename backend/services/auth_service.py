import os
from datetime import datetime, timedelta
from typing import Optional, Tuple

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from backend.repositories.doctor_repository import DoctorRepository
from backend.models.doctor import Doctor
from backend.services.audit_service import audit_service

# =====================================================
# JWT Configuration
# =====================================================

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey123changethis")
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    def __init__(self):
        self.doctor_repo = DoctorRepository()

    # =====================================================
    # Password Functions
    # =====================================================

    def get_password_hash(self, password: str) -> str:
        """Hash password"""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        return pwd_context.verify(plain_password, hashed_password)

    # =====================================================
    # Token Creation
    # =====================================================

    def create_access_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None,
    ) -> str:

        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode.update(
            {
                "exp": expire,
                "type": "access",
            }
        )

        print("=" * 60)
        print("CREATE ACCESS TOKEN")
        print("SECRET_KEY :", SECRET_KEY)
        print("Payload    :", to_encode)
        print("=" * 60)

        encoded_jwt = jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM,
        )

        return encoded_jwt

    def create_refresh_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None,
    ) -> str:

        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                days=REFRESH_TOKEN_EXPIRE_DAYS
            )

        to_encode.update(
            {
                "exp": expire,
                "type": "refresh",
            }
        )

        encoded_jwt = jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM,
        )

        return encoded_jwt

    # =====================================================
    # Token Verification
    # =====================================================

    def verify_token(
        self,
        token: str,
        token_type: str = "access",
    ) -> Optional[dict]:

        try:

            print("=" * 60)
            print("VERIFY TOKEN")
            print("SECRET_KEY :", SECRET_KEY)
            print("Incoming Token :", token)

            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM],
            )

            print("Decoded Payload :", payload)

            if payload.get("type") != token_type:
                print("Token Type Mismatch")
                return None

            return payload

        except JWTError as e:
            print("JWT ERROR :", e)
            return None

        except Exception as e:
            print("UNKNOWN ERROR :", e)
            return None

    # =====================================================
    # Register Doctor
    # =====================================================

    def register_doctor(
        self,
        db: Session,
        email: str,
        password: str,
        full_name: str,
        specialty: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> Tuple[Optional[Doctor], Optional[str]]:

        existing = self.doctor_repo.get_by_email(db, email)

        if existing:
            return None, "Email address is already registered."

        hashed_password = self.get_password_hash(password)

        new_doctor = Doctor(
            email=email,
            password_hash=hashed_password,
            full_name=full_name,
            specialty=specialty,
        )

        created_doctor = self.doctor_repo.create(db, new_doctor)

        audit_service.log_action(
            db,
            created_doctor.id,
            "doctor_register",
            ip_address,
        )

        return created_doctor, None

    # =====================================================
    # Login
    # =====================================================

    def authenticate_doctor(
        self,
        db: Session,
        email: str,
        password: str,
        ip_address: Optional[str] = None,
    ) -> Tuple[Optional[Doctor], Optional[str]]:

        doctor = self.doctor_repo.get_by_email(db, email)

        if not doctor:
            audit_service.log_action(
                db,
                None,
                f"failed_login_attempt: {email}",
                ip_address,
            )
            return None, "Invalid clinical email or password."

        if not self.verify_password(password, doctor.password_hash):
            audit_service.log_action(
                db,
                doctor.id,
                "failed_password_attempt",
                ip_address,
            )
            return None, "Invalid clinical email or password."

        audit_service.log_action(
            db,
            doctor.id,
            "doctor_login",
            ip_address,
        )

        return doctor, None


# =====================================================
# Singleton
# =====================================================

auth_service = AuthService()