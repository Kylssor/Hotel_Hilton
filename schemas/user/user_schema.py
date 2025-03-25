import uuid
from pydantic import BaseModel, Field

class UserCreateSchema(BaseModel):
    name: str = Field(..., max_length=45)
    last_name: str = Field(...)
    email: str = Field(..., max_length=100)
    password: str = Field(..., min_length=8)

class UserResponseSchema(BaseModel):
    id: uuid.UUID
    name: str
    last_name: str
    email: str

    class Config:
        json_schema_extra = {
            "example":{
                "id": "123e4567-e89b-12d3-a456-426",
                "name": "Gustavo",
                "last_name": "Romero",
                "email": "example@example.com"
            }
        }
        from_attributes = True 
        