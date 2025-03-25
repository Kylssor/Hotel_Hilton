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
                "name": "Gustavo",
                "last_name": "Romero",
                "email": "example@example.com",
                "password": "217d2c34d529d04d84d09df19e7efd63fa2d619d21e4941536450f569cffd40b",
            }
        }
        from_attributes = True 
        