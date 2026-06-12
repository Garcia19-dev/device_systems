# app/services/user_services.py

from typing import List, Optional
from fastapi import HTTPException

# Asegúrate de que 'db' en connection.py sea una instancia de Session o SessionLocal activa
from app.database.connection import db 
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate, UserPatch


# ─────────────────────────────────────────────
# Helpers internos
# ─────────────────────────────────────────────

def _email_exists(email: str) -> bool:
    """Verifica si el email ya existe."""
    user = db.query(User).filter(User.email == email).first()
    return user is not None


def _to_response(user: User) -> UserResponse:
    """Convierte un modelo de SQLAlchemy a un esquema de Pydantic."""
    # Usamos model_validate si usas Pydantic v2 con from_attributes=True en la config del Schema
    return UserResponse.model_validate(user)


# ─────────────────────────────────────────────
# Servicios
# ─────────────────────────────────────────────

def get_all_users(
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> List[UserResponse]:
    """Obtiene todos los usuarios aplicando filtros opcionales."""
    query = db.query(User)
    
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
        
    users = query.all()
    return [_to_response(user) for user in users]


def get_user_by_id(user_id: int) -> UserResponse:
    """Obtiene un usuario por ID."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "message": "Usuario no encontrado",
                "status_code": 404,
            },
        )

    return _to_response(user)


def create_user(data: UserCreate) -> UserResponse:
    """Crea un nuevo usuario."""
    if _email_exists(data.email):
        raise HTTPException(
            status_code=400,
            detail={
                "error": True,
                "message": f"El correo '{data.email}' ya está registrado",
                "status_code": 400,
            },
        )

    new_user = User(
        name=data.name,
        email=data.email,
        password=data.password,
        role=data.role,
        is_active=data.is_active,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return _to_response(new_user)


def update_user(user_id: int, data: UserUpdate) -> UserResponse:
    """Actualiza completamente un usuario."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "message": "Usuario no encontrado",
                "status_code": 404,
            },
        )

    # Validar que el nuevo correo no le pertenezca a OTRO usuario diferente
    email_owner = db.query(User).filter(User.email == data.email).first()
    if email_owner and email_owner.id != user_id:
        raise HTTPException(
            status_code=400,
            detail={
                "error": True,
                "message": f"El correo '{data.email}' ya está en uso",
                "status_code": 400,
            },
        )

    user.name = data.name
    user.email = data.email
    user.role = data.role
    user.is_active = data.is_active
    
    db.commit()
    db.refresh(user)

    return _to_response(user)


def partial_update_user(
    user_id: int,
    data: UserPatch,
) -> UserResponse:
    """Actualiza parcialmente un usuario (PATCH)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "message": "Usuario no encontrado",
                "status_code": 404,
            },
        )   

    payload = data.model_dump(exclude_none=True)

    if not payload:
        raise HTTPException(
            status_code=400,
            detail={
                "error": True,
                "message": "Debes enviar al menos un campo",
                "status_code": 400,
            },
        )

    if "email" in payload:
        email_owner = db.query(User).filter(User.email == payload["email"]).first()
        if email_owner and email_owner.id != user_id:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": True,
                    "message": f"El correo '{payload['email']}' ya está en uso",
                    "status_code": 400,
                },
            )

    # En SQLAlchemy puro se actualizan los atributos directamente sobre el objeto mapeado
    for key, value in payload.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return _to_response(user)


def delete_user(user_id: int) -> dict:
    """Elimina un usuario."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "message": "Usuario no encontrado",
                "status_code": 404,
            },
        )

    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado correctamente"}


def get_user_by_email(email: str) -> UserResponse:
    """Obtiene un usuario por email."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "message": "Usuario no encontrado",
                "status_code": 404,
            },
        )
    return _to_response(user)


def get_user_by_role(role: str) -> List[UserResponse]:
    """Obtiene usuarios por rol."""
    users = db.query(User).filter(User.role == role).all()
    return [_to_response(user) for user in users]


def get_user_by_is_active(is_active: bool) -> List[UserResponse]:
    """Obtiene usuarios por su estado de actividad."""
    users = db.query(User).filter(User.is_active == is_active).all()
    return [_to_response(user) for user in users] 


def order_by_name_or_data_created(name: str) -> List[UserResponse]:
    """Obtiene usuarios por correspondencia de nombre."""
    users = db.query(User).filter(User.name == name).all()
    return [_to_response(user) for user in users]