# app/services/user_services.py
    
from typing import List, Optional
from fastapi import HTTPException

from app.data.user_db import users_db
import app.data.user_db as db_module

from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserPartialUpdate,
    UserResponse,
)

# ─────────────────────────────────────────────

# Helpers internos

# ─────────────────────────────────────────────

def _email_exists(email: str, exclude_id: Optional[int] = None) -> bool:
    """Verifica si el email ya existe."""
    for uid, user in users_db.items():
        if user["email"] == email and uid != exclude_id:
            return True

    return False


def _to_response(user: dict) -> UserResponse:
    return UserResponse(**user)

# ─────────────────────────────────────────────

# Servicios

# ─────────────────────────────────────────────

def get_all_users(
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> List[UserResponse]:
    """Obtiene todos los usuarios."""
    result = list(users_db.values())

    if role is not None:
        result = [u for u in result if u["role"] == role]

    if is_active is not None:
        result = [u for u in result if u["is_active"] == is_active]

    return [_to_response(user) for user in result]


def get_user_by_id(user_id: int) -> UserResponse:
    """Obtiene un usuario por ID."""
    user = users_db.get(user_id)

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

    new_id = db_module.next_user_id
    db_module.next_user_id += 1

    new_user = {
        "id": new_id,
        "name": data.name,
        "email": data.email,
        "role": data.role,
        "is_active": data.is_active,
    }

    users_db[new_id] = new_user

    return _to_response(new_user)


def update_user(user_id: int, data: UserUpdate) -> UserResponse:
    """Actualiza completamente un usuario."""
    if user_id not in users_db:
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "message": "Usuario no encontrado",
                "status_code": 404,
            },
        )

    if _email_exists(data.email, exclude_id=user_id):
        raise HTTPException(
            status_code=400,
            detail={
                "error": True,
                "message": f"El correo '{data.email}' ya está en uso",
                "status_code": 400,
            },
        )

    updated_user = {
        "id": user_id,
        "name": data.name,
        "email": data.email,
        "role": data.role,
        "is_active": data.is_active,
    }

    users_db[user_id] = updated_user

    return _to_response(updated_user)


def partial_update_user(
    user_id: int,
    data: UserPartialUpdate,
) -> UserResponse:
    """Actualiza parcialmente un usuario."""
    if user_id not in users_db:
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

    if "email" in payload and _email_exists(payload["email"], exclude_id=user_id):
        raise HTTPException(
            status_code=400,
            detail={
                "error": True,
                "message": f"El correo '{payload['email']}' ya está en uso",
                "status_code": 400,
            },
        )

    users_db[user_id].update(payload)

    return _to_response(users_db[user_id])


def delete_user(user_id: int) -> None:
    """Elimina un usuario."""
    if user_id not in users_db:
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "message": "Usuario no encontrado",
                "status_code": 404,
            },
        )

    del users_db[user_id]
