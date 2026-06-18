# pyrefly: ignore [missing-import]
from fastapi import HTTPException, Header, Query
from typing import Optional

from app.data.user_db import users_db
from app.schemas.user_schema import ALLOWED_ROLES


# ─────────────────────────────────────────────
# Dependencia: obtener usuario por ID o 404
# ─────────────────────────────────────────────

def get_user_or_404(user_id: int) -> dict:
    """
    Dependencia reutilizable que busca un usuario por ID.
    Lanza 404 si no existe.
    """
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
    return user


# ─────────────────────────────────────────────
# Dependencia: validar que un rol sea permitido
# ─────────────────────────────────────────────

def validate_role(role: Optional[str] = Query(default=None)) -> Optional[str]:
    """
    Dependencia para validar el parámetro de filtro 'role' en GET /users.
    Si se pasa un rol inválido, lanza 400.
    """
    if role is not None and role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=400,
            detail={
                "error": True,
                "message": f"Rol no permitido. Roles válidos: {sorted(ALLOWED_ROLES)}",
                "status_code": 400,
            },
        )
    return role


# ─────────────────────────────────────────────
# Dependencia: validar que el email no esté duplicado
# ─────────────────────────────────────────────

def check_email_not_duplicate(email: str, exclude_id: Optional[int] = None) -> None:
    """
    Verifica que el correo no pertenezca a otro usuario.
    Lanza 400 si está duplicado.
    """
    for uid, user in users_db.items():
        if user["email"] == email and uid != exclude_id:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": True,
                    "message": f"El correo '{email}' ya está registrado",
                    "status_code": 400,
                },
            )


# ─────────────────────────────────────────────
# Dependencia: autenticación básica simulada
# ─────────────────────────────────────────────

API_KEY = "device-systems-secret-2025"


def verify_api_key(x_api_key: Optional[str] = Header(default=None)) -> str:
    """
    Simulación de autenticación básica mediante cabecera HTTP.
    Uso: incluir en la petición el header:  X-Api-Key: device-systems-secret-2025
    En producción real se usaría OAuth2 / JWT.
    """
    if x_api_key is None or x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail={
                "error": True,
                "message": "API Key inválida o no proporcionada",
                "status_code": 401,
            },
        )
    return x_api_key


# ─────────────────────────────────────────────
# Dependencia: configuración general de la API
# ─────────────────────────────────────────────

def get_api_config() -> dict:
    """Retorna configuración general de la API (simula lectura de settings)."""
    return {
        "project": "device_systems",
        "version": "2.0.0",
        "allowed_roles": sorted(ALLOWED_ROLES),
        "max_users": 1000,
    }