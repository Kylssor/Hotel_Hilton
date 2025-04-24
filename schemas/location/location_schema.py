import uuid
from pydantic import BaseModel
from uuid import UUID

class LocationCreate(BaseModel):
    name: str
    address: str
    phone: str
    city_id: uuid.UUID

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Hotel Hilton Medellín",
                "address": "Carrera 43A #1-50, Medellín",
                "phone": "+57 4 4440000",
                "city_id": "456e7890-e89b-12d3-a456-426614174000"
            }
        }


class LocationRead(BaseModel):
    id: uuid.UUID
    name: str
    address: str
    phone: str
    city_id: uuid.UUID

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": "789e4567-e89b-12d3-a456-426614174000",
                "name": "Hotel Hilton Medellín",
                "address": "Carrera 43A #1-50, Medellín",
                "phone": "+57 4 4440000",
                "city_id": "456e7890-e89b-12d3-a456-426614174000"
            }
        }


class CountrySchema(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Colombia"
            }
        }

class CitySchema(BaseModel):
    id: UUID
    name: str
    country_id: UUID

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": "456e7890-e89b-12d3-a456-426614174000",
                "name": "Medellín",
                "country_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }
