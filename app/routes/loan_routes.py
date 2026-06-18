from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional

from app.schemas.loan_schema import (
    LoanCreate,
    LoanResponse,
    LoanDetailResponse
)

from app.services.loan_service import (
    get_all_loans,
    get_loan_by_id,
    create_loan,
    return_loan,
    get_loans_by_user,
    get_loans_by_device
)

router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)


# GET /loans - Listar todos los préstamos con filtros
@router.get(
    "/", 
    response_model=List[LoanDetailResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar préstamos",
    description="Retorna la lista completa de préstamos con filtros opcionales."
)
def get_loans(
    status: Optional[str] = Query(None, description="Filtrar por estado (active, returned, overdue)"),
    user_email: Optional[str] = Query(None, description="Filtrar por email de usuario"),
    device_type: Optional[str] = Query(None, description="Filtrar por tipo de dispositivo")
):
    return get_all_loans(status=status, user_email=user_email, device_type=device_type)


# GET /loans/details - Listar préstamos con detalles (alias de /)
@router.get(
    "/details", 
    response_model=List[LoanDetailResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar préstamos con detalles",
    description="Retorna la lista completa de préstamos con detalles de usuario y dispositivo."
)
def get_loans_details(
    status: Optional[str] = Query(None, description="Filtrar por estado (active, returned, overdue)"),
    user_email: Optional[str] = Query(None, description="Filtrar por email de usuario"),
    device_type: Optional[str] = Query(None, description="Filtrar por tipo de dispositivo")
):
    return get_all_loans(status=status, user_email=user_email, device_type=device_type)


# GET /loans/{id} - Obtener un préstamo por ID
@router.get(
    "/{id}", 
    response_model=LoanDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener préstamo",
    description="Retorna un préstamo específico por su ID con detalles."
)
def get_loan_by_id_route(id: int):
    return get_loan_by_id(loan_id=id)


# POST /loans - Crear un nuevo préstamo
@router.post(
    "/", 
    response_model=LoanDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear préstamo",
    description="Crea un nuevo préstamo. Valida usuario, dispositivo y disponibilidad."
)
def create_loan_route(loan: LoanCreate):
    return create_loan(data=loan)


# PATCH /loans/{id}/return - Devolver un préstamo
@router.patch(
    "/{id}/return", 
    response_model=LoanDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Devolver préstamo",
    description="Devuelve un préstamo, cambia el estado a returned y libera el dispositivo."
)
def return_loan_route(id: int):
    return return_loan(loan_id=id)


# GET /users/{id}/loans - Obtener préstamos de un usuario
@router.get(
    "/users/{user_id}/loans", 
    response_model=List[LoanDetailResponse],
    status_code=status.HTTP_200_OK,
    summary="Préstamos de usuario",
    description="Retorna todos los préstamos de un usuario específico."
)
def get_user_loans(user_id: int):
    return get_loans_by_user(user_id=user_id)


# GET /devices/{id}/loans - Obtener préstamos de un dispositivo
@router.get(
    "/devices/{device_id}/loans", 
    response_model=List[LoanDetailResponse],
    status_code=status.HTTP_200_OK,
    summary="Préstamos de dispositivo",
    description="Retorna todos los préstamos de un dispositivo específico."
)
def get_device_loans(device_id: int):
    return get_loans_by_device(device_id=device_id)

