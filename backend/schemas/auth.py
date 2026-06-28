from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class DoctorRegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="Doctor's clinical email address")
    password: str = Field(..., min_length=8, description="Security password (min 8 chars)")
    full_name: str = Field(..., description="Doctor's full name")
    specialty: Optional[str] = Field(None, description="Clinical specialty")

class DoctorLoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Doctor's clinical email address")
    password: str = Field(..., description="Security password")

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str
    type: str
    exp: int
