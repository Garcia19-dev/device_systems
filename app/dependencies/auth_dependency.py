from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from app.dependencies.database_dependency import get_db
from app.auth.security import decode_access_token
from app.models.user_model import User

# Le dice a FastAPI que busque el token en la cabecera 'Authorization: Bearer <token>'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_access_token(token)
        if payload is None:
            print("❌ Token inválido o expirado")
            raise credentials_exception
        
        email: str = payload.get("sub")
        if email is None:
            print("❌ Token no contiene 'sub' (email)")
            raise credentials_exception
            
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            print(f"❌ Usuario con email {email} no encontrado")
            raise credentials_exception
            
        print(f"✅ Usuario autenticado: {user.email}")
        return user
        
    except JWTError as e:
        print(f"❌ Error JWT: {e}")
        raise credentials_exception
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        raise credentials_exception

def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo"
        )
    print(f"✅ Usuario activo: {current_user.email}")
    return current_user

# Generador de permisos por Roles
class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_active_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes los permisos necesarios para realizar esta acción"
            )
        print(f"✅ Usuario con rol {current_user.role} autorizado")
        return current_user