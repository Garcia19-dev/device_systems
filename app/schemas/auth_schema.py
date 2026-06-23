from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
import re

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = Field(default="user")

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if ' ' in v:
            raise ValueError('La contraseña no debe contener espacios en blanco')
        if not re.search(r'[A-Z]', v):
            raise ValueError('La contraseña debe tener al menos una mayúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('La contraseña debe tener al menos una minúscula')
        if not re.search(r'[0-9]', v):
            raise ValueError('La contraseña debe tener al menos un número')
        return v

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        roles_permitidos = ['admin', 'support', 'user']
        if v not in roles_permitidos:
            raise ValueError(f'Rol no permitido. Roles válidos: {roles_permitidos}')
        return v

class UserLogin(BaseModel):
    username: str # OAuth2 de FastAPI usa 'username' (aquí irá el email)
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str = None
    role: str = None