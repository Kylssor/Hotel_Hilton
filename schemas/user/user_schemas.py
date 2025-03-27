from typing import Optional
import uuid
from pydantic import BaseModel, Field

class UserCreateSchema(BaseModel):
    identification_number: str = Field(default=None, nullable=False, max_length=20)
    first_name: str = Field(default=None, nullable=False, max_length=100)
    last_name: str = Field(default=None, nullable=False, max_length=100)
    email: str = Field(default=None, nullable=False, max_length=100)
    phone: str = Field(default=None, nullable=False, max_length=15)
    address: str = Field(default=None, nullable=False, max_length=200)
    city_id: uuid.UUID = Field(default=None, nullable=False)
    password: str = Field(default=None, nullable=False)

    class Config:
        json_schema_extra = {
            "example": {
                "identification_number": "1234567890",
                "first_name": "Juan",
                "last_name": "Pérez",
                "email": "juan.perez@example.com",
                "phone": "123456789",
                "address": "Calle Falsa 123, Ciudad",
                "city_id": "123e4567-e89b-12d3-a456-426614174000",
                "password": "217d2c34d529d04d84d09df19e7efd63fa2d619d21e4941536450f569cffd40b"
            }
        }

class UserResponseSchema(BaseModel):
    id: uuid.UUID = Field(default=None, nullable=False)
    first_name: str = Field(default=None, nullable=False, max_length=100)
    last_name: str = Field(default=None, nullable=False, max_length=100)
    email: str = Field(default=None, nullable=False, max_length=100)

    class Config:
        orm_mode = True

class UserSessionResponseSchema(BaseModel):
    id: uuid.UUID = Field(default=None, nullable=False)
    first_name: str = Field(default=None, nullable=False, max_length=100)
    last_name: str = Field(default=None, nullable=False, max_length=100)
    user_name: Optional[str] = Field(default=None, max_length=100)
    email: str = Field(default=None, nullable=False, max_length=100)
    role: str = Field(default=None, nullable=False, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "first_name": "Gustavo",
                "last_name": "Romero",
                "user_name": "GusRom",
                "email": "example@example.com",
                "role": "admin"
            }
        }
