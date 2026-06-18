import sqlalchemy as sa
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Device(Base):
    __tablename__ = "devices"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, index=True)
    serial_number = sa.Column(sa.String, unique=True, nullable=False)
    device_type = sa.Column(sa.String, nullable=False)
    brand = sa.Column(sa.String, index=True, nullable=True)
    is_available = sa.Column(sa.Boolean, default=True)
    created_at = sa.Column(sa.DateTime, default=sa.func.now())

    loans = relationship("Loan", back_populates="device")