# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, status
from typing import List, Optional

from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserPatch,
    UserResponse,
)

import app.services.user_services as user_service

from app.dependencies.user_dependencies import ( # type: ignore
    get_user_or_404,
    validate_role,
)

router = APIRouter(prefix="/users", tags=["Users"])


# ─────────────────────────────────────────────
# GET /users  – Listar todos los usuarios
# ─────────────────────────────────────────────

@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description=(
        "Retorna la lista completa de usuarios registrados. "
        "Se puede filtrar por **role** y/o **is_active** mediante query params."
    ),
    response_description="Lista de usuarios encontrados",
)
def list_users(
    role: Optional[str] = Depends(validate_role),
    is_active: Optional[bool] = None,
):
    return user_service.get_all_users(role=role, is_active=is_active)


# ─────────────────────────────────────────────
# GET /users/{user_id}  – Consultar usuario por ID
# ─────────────────────────────────────────────

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por ID",
    description="Retorna los datos de un usuario específico identificado por su **user_id**.",
    response_description="Datos del usuario encontrado",
)
def get_user(user: dict = Depends(get_user_or_404)):
    return UserResponse(**user)


# ─────────────────────────────────────────────
# POST /users  – Crear usuario
# ─────────────────────────────────────────────

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description=(
        "Crea un nuevo usuario en el sistema. "
        "El correo debe ser único y el rol debe ser uno de los permitidos: "
        "`admin`, `viewer`, `support`, `editor`."
    ),
    response_description="Usuario creado exitosamente",
)
def create_user(data: UserCreate):
    return user_service.create_user(data)


# ─────────────────────────────────────────────
# PUT /users/{user_id}  – Actualización completa
# ─────────────────────────────────────────────

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario completo (PUT)",
    description=(
        "Reemplaza **completamente** la información de un usuario. "
        "Se deben enviar **todos** los campos: `name`, `email`, `role`, `is_active`."
    ),
    response_description="Usuario actualizado correctamente",
)
def update_user(data: UserUpdate, user: dict = Depends(get_user_or_404)):
    return user_service.update_user(user["id"], data)


# ─────────────────────────────────────────────
# PATCH /users/{user_id}  – Actualización parcial
# ─────────────────────────────────────────────

@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario parcialmente (PATCH)",
    description=(
        "Actualiza **solo los campos enviados** de un usuario. "
        "Si no se envía ningún campo, responde con **400 Bad Request**."
    ),
    response_description="Usuario actualizado parcialmente",
)
def partial_update_user(data: UserPatch, user: dict = Depends(get_user_or_404)):
    return user_service.partial_update_user(user["id"], data)


# ─────────────────────────────────────────────
# DELETE /users/{user_id}  – Eliminar usuario
# ─────────────────────────────────────────────

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar usuario",
    description="Elimina un usuario del sistema por su **user_id**. Retorna mensaje de confirmación.",
    response_description="Confirmación de eliminación",
)
def delete_user(user: dict = Depends(get_user_or_404)):
    user_service.delete_user(user["id"])
    return {
        "error": False,
        "message": f"Usuario con ID {user['id']} eliminado correctamente",
        "status_code": 200,
    }
