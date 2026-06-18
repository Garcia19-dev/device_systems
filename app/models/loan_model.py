import sqlalchemy as sa
from sqlalchemy.orm import relationship
from app.database.connection import Base
from sqlalchemy import ForeignKey

class Loan(Base):
    __tablename__ = "loans"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    user_id = sa.Column(sa.Integer, ForeignKey("users.id"), index=True)
    device_id = sa.Column(sa.Integer, ForeignKey("devices.id"), index=True)
    loan_date = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    return_date = sa.Column(sa.DateTime, nullable=True)
    status = sa.Column(sa.String, nullable=False, default="active")
    
    user = relationship("User", back_populates="loans")
    device = relationship("Device", back_populates="loans")
