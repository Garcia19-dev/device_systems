from fastapi import APIRouter, HTTPException, Query, Response
from app.schemas.user_schema import UserCreate, UserResponse
from typing import List, Optional

router = APIRouter()

# DB simulada
users_db = [
    {
        "id": 1,
        "name": "Juan",
        "email": "juan@example.com",
        "role": "admin",
        "is_active": True
    },
    {
        "id": 2,
        "name": "Maria",
        "email": "maria@example.com",
        "role": "user",
        "is_active": False
    },
    {
        "id": 3,
        "name": "Pedro",
        "email": "pedro@example.com",
        "role": "user",
        "is_active": False
    },
    {
        "id": 4,
        "name": "Ana",
        "email": "ana@example.com",
        "role": "user",
        "is_active": True
    },
    {
        "id": 5,
        "name": "Luis",
        "email": "luis@example.com",
        "role": "admin",
        "is_active": True
    }
]



# GET /users
@router.get("/users", response_model=List[UserResponse])
def get_users(
    response: Response,
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None)
):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    filtered_users = users_db

    if role is not None:
        filtered_users = [
            user for user in filtered_users
            if user["role"] == role
        ]

    if is_active is not None:
        filtered_users = [
            user for user in filtered_users
            if user["is_active"] == is_active
        ]

    return filtered_users


# GET /users/{user_id}
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    for user in users_db:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

# GET /users?is_active=true
@router.get("/users", response_model=List[UserResponse])
def get_users_by_active(
    response: Response,
    is_active: bool = Query(..., description="Filtrar por estado activo")
):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    filtered_users = [
        user for user in users_db
        if user["is_active"] == is_active
    ]

    return filtered_users


# POST /users
@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    # Validar correo duplicado
    for existing_user in users_db:
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=400,
                detail="El correo ya está registrado"
            )

    new_user = {
        "id": len(users_db) + 1,
        **user.model_dump()
    }

    users_db.append(new_user)

    return new_user