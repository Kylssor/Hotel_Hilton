from pydantic import BaseModel
from uuid import UUID

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
