# app/main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# 1. Importamos la función de creación de tablas y el modelo para que SQLAlchemy lo registre
from app.database.connection import create_tables
from app.models.user_model import User  # ¡Crucial para que detecte la tabla 'users'!

from app.routes.user_routes import router as user_router

# 2. Ejecutamos la creación automática de tablas antes de instanciar la API
create_tables()

# ─────────────────────────────────────────────
# Metadatos de la API (Swagger / OpenAPI)
# ─────────────────────────────────────────────

description = """
## device_systems API 🖥️

API REST para la **gestión de usuarios** del sistema device_systems.

### Funcionalidades
- ✅ Listar y consultar usuarios
- ✅ Crear nuevos usuarios
- ✅ Actualización completa (PUT) y parcial (PATCH)
- ✅ Eliminación de usuarios
- ✅ Filtros por rol y estado
- ✅ Validaciones con Pydantic v2
- ✅ Manejo de errores con HTTPException
- ✅ Dependency Injection con Depends()
- ✅ Uso de SQLAlchemy para la gestión de la base de datos

### Roles permitidos
`admin` |  `editor` | `user`
"""

tags_metadata = [
    {
        "name": "Users",
        "description": "Operaciones CRUD completas sobre el recurso **usuarios**.",
    },
]

app = FastAPI(
    title="device_systems API",
    description=description,
    version="2.0.0",
    contact={
        "name": "Equipo device_systems",
        "email": "dev@devicesystems.com",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─────────────────────────────────────────────
# Manejador global de excepciones no controladas
# ─────────────────────────────────────────────

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Error interno del servidor",
            "status_code": 500,
        },
    )


# ─────────────────────────────────────────────
# Registro de routers
# ─────────────────────────────────────────────

app.include_router(user_router)


# ─────────────────────────────────────────────
# Endpoint raíz
# ─────────────────────────────────────────────

@app.get("/", tags=["Root"], summary="Bienvenida")
def root():
    """Endpoint raíz de la API. Confirma que el servidor está activo."""
    return {
        "project": "device_systems",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "running ✅",
    }