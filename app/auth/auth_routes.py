from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.dependencies.database_dependency import get_db
from app.auth.security import verify_password, create_access_token, get_password_hash
from app.dependencies.auth_dependency import get_current_user, get_current_active_user, RoleChecker
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserResponse

# Importar el limiter desde main.py
from app.main import limiter

router = APIRouter(prefix="/auth", tags=["auth"])

# Función auxiliar
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# ─────────────────────────────────────────────
# POST /auth/register - Registro de usuario
# ─────────────────────────────────────────────
@router.post("/register", summary="Registrar nuevo usuario", response_model=UserResponse)
@limiter.limit("3/minute")
def register(
    request: Request,
    user_data: UserCreate,  # O usa los campos directamente
    db: Session = Depends(get_db)
):
    """
    Registra un nuevo usuario en el sistema
    """
    # Verificar si el email ya existe
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Crear nuevo usuario
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password,
        role=user_data.role if hasattr(user_data, 'role') else "user",
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

# ─────────────────────────────────────────────
# POST /auth/login
# ─────────────────────────────────────────────
@router.post("/login")
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Inicia sesión y retorna un token JWT
    """
    user = get_user_by_email(db, form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar si el usuario está activo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ─────────────────────────────────────────────
# GET /auth/me - Obtener perfil del usuario
# ─────────────────────────────────────────────
@router.get("/me", summary="Obtener perfil actual")
def get_me(
    current_user: User = Depends(get_current_active_user)  # Usa get_current_active_user
):
    """
    Retorna la información del usuario autenticado
    🔒 Requiere: Authorization: Bearer <token>
    """
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at if hasattr(current_user, 'created_at') else None
    }

# ─────────────────────────────────────────────
# GET /auth/admin-only - Solo administradores
# ─────────────────────────────────────────────
@router.get("/admin-only", summary="Solo para administradores")
def admin_endpoint(
    current_user: User = Depends(RoleChecker(["admin"]))
):
    """
    Endpoint exclusivo para administradores
    🔒 Requiere: Rol 'admin'
    """
    return {
        "message": f"Hola admin {current_user.email}",
        "role": current_user.role,
        "user_id": current_user.id
    }

# ─────────────────────────────────────────────
# GET /auth/protected - Admin o User
# ─────────────────────────────────────────────
@router.get("/protected", summary="Para admin o user")
def protected_endpoint(
    current_user: User = Depends(RoleChecker(["admin", "user"]))
):
    """
    Endpoint accesible para administradores y usuarios normales
    🔒 Requiere: Rol 'admin' o 'user'
    """
    return {
        "message": f"Bienvenido {current_user.email}",
        "role": current_user.role,
        "user_id": current_user.id
    }

# ─────────────────────────────────────────────
# GET /auth/users - Solo administradores (lista de usuarios)
# ─────────────────────────────────────────────
@router.get("/users", summary="Listar todos los usuarios (solo admin)")
def list_users(
    current_user: User = Depends(RoleChecker(["admin"])),
    db: Session = Depends(get_db)
):
    """
    Lista todos los usuarios del sistema
    🔒 Requiere: Rol 'admin'
    """
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active
        }
        for user in users
    ]

# ─────────────────────────────────────────────
# PUT /auth/users/{user_id}/toggle-active - Solo admin
# ─────────────────────────────────────────────
@router.put("/users/{user_id}/toggle-active", summary="Activar/desactivar usuario")
def toggle_user_active(
    user_id: int,
    current_user: User = Depends(RoleChecker(["admin"])),
    db: Session = Depends(get_db)
):
    """
    Activa o desactiva un usuario (solo administradores)
    🔒 Requiere: Rol 'admin'
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)
    
    return {
        "message": f"Usuario {user.email} {'activado' if user.is_active else 'desactivado'}",
        "user_id": user.id,
        "is_active": user.is_active
    }