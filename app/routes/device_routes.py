from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.connection import db
from app.models.device_model import Device

from app.schemas.device_schema import (
    DeviceCreate,
    DeviceUpdate,
    DevicePatch,
    DeviceResponse
)

from app.services.device_service import (
    get_all_devices,
    get_device_by_id,
    create_device,
    update_device,
    partial_update_device,
    delete_device
)

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


# GET /devices - Listar todos los dispositivos con filtros
@router.get(
    "/", 
    response_model=List[DeviceResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar dispositivos",
    description="Retorna la lista completa de dispositivos registrados con filtros opcionales."
)
def get_devices(
    device_type: Optional[str] = Query(None, description="Filtrar por tipo de dispositivo"),
    brand: Optional[str] = Query(None, description="Filtrar por marca"),
    is_available: Optional[bool] = Query(None, description="Filtrar por disponibilidad"),
    search: Optional[str] = Query(None, description="Buscar por nombre, marca o número de serie")
):
    return get_all_devices(device_type=device_type, brand=brand, is_available=is_available, search=search)

# GET /devices/{id} - Obtener un dispositivo por ID
@router.get(
    "/{id}", 
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener dispositivo",
    description="Retorna un dispositivo específico por su ID."
)
def get_device_by_id_route(id: int):
    return get_device_by_id(device_id=id)

# POST /devices - Crear un nuevo dispositivo
@router.post(
    "/", 
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dispositivo",
    description="Crea un nuevo dispositivo en el sistema."
)
def create_device_route(device: DeviceCreate):
    return create_device(data=device)

# PUT /devices/{id} - Actualizar un dispositivo
@router.put(
    "/{id}", 
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar dispositivo",
    description="Actualiza la información de un dispositivo existente."
)
def update_device_route(id: int, device: DeviceUpdate):
    return update_device(device_id=id, data=device)

# PATCH /devices/{id} - Actualizar parcialmente un dispositivo
@router.patch(
    "/{id}", 
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar parcialmente dispositivo",
    description="Actualiza parcialmente la información de un dispositivo existente."
)
def update_device_partial_route(id: int, device: DevicePatch):
    return partial_update_device(device_id=id, data=device)

# DELETE /devices/{id} - Eliminar un dispositivo
@router.delete(
    "/{id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar dispositivo",
    description="Elimina un dispositivo del sistema."
)
def delete_device_route(id: int):
    delete_device(device_id=id)
    return None
