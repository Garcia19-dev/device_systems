from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./database.db"
)

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# 1. Cambiamos el nombre a SessionLocal (es la fábrica de sesiones)
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# 2. ¡AQUÍ ESTÁ EL TRUCO! Creamos la sesión activa llamada 'db'
# Esto es lo que tu 'user_services.py' está intentando usar para hacer las consultas
db = SessionLocal()

class Base(DeclarativeBase):
    pass

def create_tables():
    Base.metadata.create_all(bind=engine)