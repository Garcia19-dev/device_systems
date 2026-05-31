# app/schemas/user_schema.py

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

# Roles permitidos
ALLOWED_ROLES = {"admin", "viewer", "support", "editor", "user"}

class UserCreate(BaseModel):
    """Schema para crear usuarios (POST)."""
    name: str
    email: EmailStr
    role: str
    is_active: bool = True

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in ALLOWED_ROLES:
            raise ValueError(
                f"Rol no permitido. Roles válidos: {sorted(ALLOWED_ROLES)}"
            )
        return v

class UserUpdate(BaseModel):
    """Schema para actualización completa (PUT)."""
    name: str
    email: EmailStr
    role: str
    is_active: bool

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in ALLOWED_ROLES:
            raise ValueError(
                f"Rol no permitido. Roles válidos: {sorted(ALLOWED_ROLES)}"
            )
        return v

class UserPartialUpdate(BaseModel):
    """Schema para actualización parcial (PATCH)."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip() if v else v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ALLOWED_ROLES:
            raise ValueError(
                f"Rol no permitido. Roles válidos: {sorted(ALLOWED_ROLES)}"
            )
        return v

class UserResponse(BaseModel):
    """Schema de respuesta."""
    id: int
    name: str
    email: str
    role: str
    is_active: bool

    model_config = {
        "from_attributes": True
    }

class ErrorResponse(BaseModel):
    """Schema para errores."""
    error: bool = True
    message: str
    status_code: int
