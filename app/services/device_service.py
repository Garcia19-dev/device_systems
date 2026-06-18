# app/services/device_service.py

from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import or_

# Asegúrate de que 'db' en connection.py sea una instancia de Session o SessionLocal activa
from app.database.connection import db 
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceResponse, DeviceUpdate, DevicePatch


# ─────────────────────────────────────────────
# Helpers internos
# ─────────────────────────────────────────────

def _serial_number_exists(serial_number: str) -> bool:
    """Verifica si el serial_number ya existe."""
    device = db.query(Device).filter(Device.serial_number == serial_number).first()
    return device is not None


def _to_response(device: Device) -> DeviceResponse:
    """Convierte un modelo de SQLAlchemy a un esquema de Pydantic."""
    return DeviceResponse.model_validate(device)


# ─────────────────────────────────────────────
# Servicios
# ─────────────────────────────────────────────

def get_all_devices(
    device_type: Optional[str] = None,
    brand: Optional[str] = None,
    is_available: Optional[bool] = None,
    search: Optional[str] = None,
) -> List[DeviceResponse]:
    """Obtiene todos los dispositivos aplicando filtros opcionales."""
    query = db.query(Device)
    
    if device_type:
        query = query.filter(Device.device_type == device_type)
    if brand:
        query = query.filter(Device.brand == brand)
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if search:
        query = query.filter(
            or_(
                Device.name.ilike(f"%{search}%"),
                Device.brand.ilike(f"%{search}%"),
                Device.serial_number.ilike(f"%{search}%"),
            )
        )
        
    devices = query.all()
    return [_to_response(device) for device in devices]


def get_device_by_id(device_id: int) -> DeviceResponse:
    """Obtiene un dispositivo por ID."""
    device = db.query(Device).filter(Device.id == device_id).first()

    if not device:
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "message": "Dispositivo no encontrado",
                "status_code": 404,
            },
        )

    return _to_response(device)


def create_device(data: DeviceCreate) -> DeviceResponse:
    """Crea un nuevo dispositivo."""
    if _serial_number_exists(data.serial_number):
        raise HTTPException(
            status_code=400,
            detail={
                "error": True,
                "message": f"El número de serie '{data.serial_number}' ya está registrado",
                "status_code": 400,
            },
        )

    new_device = Device(
        name=data.name,
        serial_number=data.serial_number,
        device_type=data.device_type,
        brand=data.brand,
        is_available=data.is_available,
    )
    db.add(new_device)
    db.commit()
    db.refresh(new_device)

    return _to_response(new_device)


def update_device(device_id: int, data: DeviceUpdate) -> DeviceResponse:
    """Actualiza completamente un dispositivo."""
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "message": "Dispositivo no encontrado",
                "status_code": 404,
            },
        )

    # Validar que el nuevo serial no le pertenezca a OTRO dispositivo diferente
    if data.serial_number:
        serial_owner = db.query(Device).filter(Device.serial_number == data.serial_number).first()
        if serial_owner and serial_owner.id != device_id:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": True,
                    "message": f"El número de serie '{data.serial_number}' ya está en uso",
                    "status_code": 400,
                },
            )

    device.name = data.name
    device.serial_number = data.serial_number
    device.device_type = data.device_type
    device.brand = data.brand
    device.is_available = data.is_available
    
    db.commit()
    db.refresh(device)

    return _to_response(device)


def partial_update_device(
    device_id: int,
    data: DevicePatch,
) -> DeviceResponse:
    """Actualiza parcialmente un dispositivo (PATCH)."""
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "message": "Dispositivo no encontrado",
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

    if "serial_number" in payload:
        serial_owner = db.query(Device).filter(Device.serial_number == payload["serial_number"]).first()
        if serial_owner and serial_owner.id != device_id:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": True,
                    "message": f"El número de serie '{payload['serial_number']}' ya está en uso",
                    "status_code": 400,
                },
            )

    for key, value in payload.items():
        setattr(device, key, value)

    db.commit()
    db.refresh(device)

    return _to_response(device)


def delete_device(device_id: int) -> dict:
    """Elimina un dispositivo."""
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "message": "Dispositivo no encontrado",
                "status_code": 404,
            },
        )

    db.delete(device)
    db.commit()
    return {"message": "Dispositivo eliminado correctamente"}