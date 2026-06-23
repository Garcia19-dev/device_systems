# app/main.py
import time
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

# 📦 Configuración de Rate Limiting (DEBE IR AQUÍ ARRIBA)
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Se crea la instancia aquí arriba para que cuando las rutas la busquen, ya exista.
limiter = Limiter(key_func=get_remote_address)

# 🗄️ Base de Datos y Modelos
from app.database.connection import create_tables
from app.models.user_model import User  
from app.models.device_model import Device  
from app.models.loan_model import Loan  

# 🛣️ Routers (IMPORTADOS DESPUÉS DE CREAR EL LIMITER)
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.auth.auth_routes import router as auth_router 

# Ejecutamos la creación de tablas
create_tables()

# Metadatos de la API
description = "## device_systems API 🖥️\nAPI REST segura para la gestión de usuarios, dispositivos y préstamos."

app = FastAPI(
    title="device_systems API",
    description=description,
    version="3.0.0",
)

# ─────────────────────────────────────────────
# Middleware Personalizado (Fase 10)
# ─────────────────────────────────────────────
class CustomSecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        response.headers["X-Request-ID"] = request_id
        
        return response

app.add_middleware(CustomSecurityMiddleware)

# ─────────────────────────────────────────────
# Configuración CORS (Fase 9)
# ─────────────────────────────────────────────
origins = ["http://localhost:5173", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enlazar el limiter a la aplicación
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Manejador global de excepciones
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": True, "message": f"Error interno: {str(exc)}"},
    )

# Registro de routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)

@app.get("/", tags=["Root"])
def root():
    return {"project": "device_systems", "version": "3.0.0", "status": "running ✅"}