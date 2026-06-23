import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class CustomSecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Generar o capturar un ID único para la petición
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # Procesar la petición original
        response = await call_next(request)
        
        # Calcular tiempo transcurrido
        process_time = time.time() - start_time
        
        # Insertar las cabeceras requeridas en la respuesta
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        response.headers["X-Request-ID"] = request_id
        
        # Guardar registro simple en consola
        print(f"LOG: {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s")
        
        return response