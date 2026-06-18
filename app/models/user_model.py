import sqlalchemy as sa
from sqlalchemy.orm import relationship
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, index=True)
    email = sa.Column(sa.String, unique=True, index=True)
    password = sa.Column(sa.String)
    role = sa.Column(sa.String, index=True)
    is_active = sa.Column(sa.Boolean, default=True)
    created_at = sa.Column(sa.DateTime, default=sa.func.now())

    loans = relationship("Loan", back_populates="user")