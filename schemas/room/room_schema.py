from typing import Optional
import uuid
from pydantic import BaseModel

class RoomCreate(BaseModel):
    number: str
    type_id: uuid.UUID
    status_id: uuid.UUID
    price_per_night: float
    size: float
    description: Optional[str]
    tax: float
    image_url: Optional[str]
    location_id: uuid.UUID

    class Config:
        json_schema_extra = {
            "example": {
                "number": "101",
                "type_id": "222e4567-e89b-12d3-a456-426614174000",
                "status_id": "333e4567-e89b-12d3-a456-426614174000",
                "price_per_night": 150.00,
                "size": 30.0,
                "description": "Habitación estándar con cama doble",
                "tax": 10.0,
                "image_url": "https://example.com/images/room101.jpg",
                "location_id": "444e4567-e89b-12d3-a456-426614174000"
            }
        }


class RoomRead(BaseModel):
    id: uuid.UUID
    number: str
    type_id: uuid.UUID
    status_id: uuid.UUID
    price_per_night: float
    size: float
    description: Optional[str]
    tax: float
    image_url: Optional[str]
    location_id: uuid.UUID

    class Config:
        json_schema_extra = {
            "example": {
                "id": "555e4567-e89b-12d3-a456-426614174000",
                "number": "101",
                "type_id": "222e4567-e89b-12d3-a456-426614174000",
                "status_id": "333e4567-e89b-12d3-a456-426614174000",
                "price_per_night": 150.00,
                "size": 30.0,
                "description": "Habitación estándar con cama doble",
                "tax": 10.0,
                "image_url": "https://example.com/images/room101.jpg",
                "location_id": "444e4567-e89b-12d3-a456-426614174000"
            }
        }


class RoomFilter(BaseModel):
    location_id: Optional[uuid.UUID]
    type_id: Optional[uuid.UUID]
    status_id: Optional[uuid.UUID]