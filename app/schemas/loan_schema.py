from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional


class LoanCreate(BaseModel):
    user_id: int
    device_id: int


class LoanUpdate(BaseModel):
    status: Optional[str] = None

    @field_validator('status')
    @classmethod
    def status_valid(cls, v):
        if v and v not in ['active', 'returned', 'overdue']:
            raise ValueError('status debe ser: active, returned, o overdue')
        return v


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime]
    status: str

    model_config = ConfigDict(from_attributes=True)


class UserBasic(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class DeviceBasic(BaseModel):
    id: int
    name: str
    brand: str
    serial_number: str

    model_config = ConfigDict(from_attributes=True)


class LoanDetailResponse(BaseModel):
    id: int
    status: str
    loan_date: datetime
    return_date: Optional[datetime]

    user: UserBasic
    device: DeviceBasic

    model_config = ConfigDict(from_attributes=True)
