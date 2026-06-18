from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional


class DeviceBase(BaseModel):
    name: str
    serial_number: str
    device_type: str
    brand: str
    is_available: bool = True


class DeviceCreate(DeviceBase):
    @field_validator('serial_number')
    @classmethod
    def serial_number_required(cls, v):
        if not v or v.strip() == '':
            raise ValueError('serial_number es obligatorio')
        return v
    
    @field_validator('device_type')
    @classmethod
    def device_type_valid(cls, v):
        valid_types = ['laptop', 'desktop', 'tablet', 'phone', 'monitor', 'other']
        if v.lower() not in valid_types:
            raise ValueError(f'device_type debe ser uno de: {valid_types}')
        return v.lower()


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    serial_number: Optional[str] = None
    device_type: Optional[str] = None
    brand: Optional[str] = None
    is_available: Optional[bool] = None


class DevicePatch(BaseModel):
    name: Optional[str] = None
    serial_number: Optional[str] = None
    device_type: Optional[str] = None
    brand: Optional[str] = None
    is_available: Optional[bool] = None


class DeviceResponse(DeviceBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)