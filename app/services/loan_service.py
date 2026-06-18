# app/services/loan_service.py

from typing import List, Optional
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import and_, or_

from app.database.connection import db 
from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanUpdate, LoanDetailResponse, UserBasic, DeviceBasic


# ─────────────────────────────────────────────
# Helpers internos
# ─────────────────────────────────────────────

def _to_response(loan: Loan) -> LoanResponse:
    """Convierte un modelo de SQLAlchemy a un esquema de Pydantic."""
    return LoanResponse.model_validate(loan)


def _to_detail_response(loan: Loan) -> LoanDetailResponse:
    """Convierte un modelo de SQLAlchemy a un esquema de Pydantic con detalles."""
    return LoanDetailResponse(
        id=loan.id,
        status=loan.status,
        loan_date=loan.loan_date,
        return_date=loan.return_date,
        user=UserBasic.model_validate(loan.user),
        device=DeviceBasic.model_validate(loan.device)
    )


# ─────────────────────────────────────────────
# Servicios
# ─────────────────────────────────────────────

def get_all_loans(
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
) -> List[LoanDetailResponse]:
    """Obtiene todos los préstamos aplicando filtros opcionales con JOIN."""
    query = db.query(Loan).join(User).join(Device)
    
    if status:
        query = query.filter(Loan.status == status)
    if user_email:
        query = query.filter(User.email.ilike(f"%{user_email}%"))
    if device_type:
        query = query.filter(Device.device_type == device_type)
        
    loans = query.all()
    return [_to_detail_response(loan) for loan in loans]


def get_loan_by_id(loan_id: int) -> LoanDetailResponse:
    """Obtiene un préstamo por ID con detalles."""
    loan = db.query(Loan).filter(Loan.id == loan_id).first()

    if not loan:
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "message": "Préstamo no encontrado",
                "status_code": 404,
            },
        )

    return _to_detail_response(loan)


def create_loan(data: LoanCreate) -> LoanDetailResponse:
    """Crea un nuevo préstamo con validaciones de negocio."""
    # Verificar que el usuario existe
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "message": "Usuario no encontrado",
                "status_code": 404,
            },
        )

    # Verificar que el dispositivo existe
    device = db.query(Device).filter(Device.id == data.device_id).first()
    if not device:
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "message": "Dispositivo no encontrado",
                "status_code": 404,
            },
        )

    # Verificar que el dispositivo está disponible
    if not device.is_available:
        raise HTTPException(
            status_code=409,
            detail={
                "error": True,
                "message": "El dispositivo no está disponible para préstamo",
                "status_code": 409,
            },
        )

    # Crear el préstamo
    new_loan = Loan(
        user_id=data.user_id,
        device_id=data.device_id,
        loan_date=datetime.now(),
        status="active"
    )
    
    # Cambiar disponibilidad del dispositivo
    device.is_available = False
    
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    db.refresh(device)

    return _to_detail_response(new_loan)


def return_loan(loan_id: int) -> LoanDetailResponse:
    """Devuelve un préstamo (cambia estado a returned y libera dispositivo)."""
    loan = db.query(Loan).filter(Loan.id == loan_id).first()

    if not loan:
        raise HTTPException(
            status_code=404,
            detail={
                "error": True,
                "message": "Préstamo no encontrado",
                "status_code": 404,
            },
        )

    # Verificar que el préstamo no haya sido devuelto
    if loan.status == "returned":
        raise HTTPException(
            status_code=409,
            detail={
                "error": True,
                "message": "El préstamo ya fue devuelto",
                "status_code": 409,
            },
        )

    # Cambiar estado del préstamo
    loan.status = "returned"
    loan.return_date = datetime.now()
    
    # Liberar el dispositivo
    device = db.query(Device).filter(Device.id == loan.device_id).first()
    if device:
        device.is_available = True
    
    db.commit()
    db.refresh(loan)
    db.refresh(device)

    return _to_detail_response(loan)


def get_loans_by_user(user_id: int) -> List[LoanDetailResponse]:
    """Obtiene todos los préstamos de un usuario específico."""
    loans = db.query(Loan).filter(Loan.user_id == user_id).all()
    return [_to_detail_response(loan) for loan in loans]


def get_loans_by_device(device_id: int) -> List[LoanDetailResponse]:
    """Obtiene todos los préstamos de un dispositivo específico."""
    loans = db.query(Loan).filter(Loan.device_id == device_id).all()
    return [_to_detail_response(loan) for loan in loans]

