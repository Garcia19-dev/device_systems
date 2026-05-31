# app/data/users_db.py

from typing import Dict

# Base de datos simulada

users_db: Dict[int, Dict] = {
1: {
"id": 1,
"name": "Juan",
"email": "juan@example.com",
"role": "admin",
"is_active": True
},
2: {
"id": 2,
"name": "Maria",
"email": "maria@example.com",
"role": "user",
"is_active": False
},
3: {
"id": 3,
"name": "Pedro",
"email": "pedro@example.com",
"role": "user",
"is_active": False
},
4: {
"id": 4,
"name": "Ana",
"email": "ana@example.com",
"role": "viewer",
"is_active": True
},
5: {
"id": 5,
"name": "Luis",
"email": "luis@example.com",
"role": "support",
"is_active": True
}
}

# Contador incremental de IDs

next_user_id: int = 6
