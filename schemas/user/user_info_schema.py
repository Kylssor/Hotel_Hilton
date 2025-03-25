from typing import Optional
import uuid
from pydantic import BaseModel, Field


class UserInfoSchema(BaseModel):
    id: uuid.UUID
    name: str = Field(..., max_length=45)
    last_name: str = Field(..., max_length=100)
    email: str = Field(..., max_length=100)
    
    class Config:
        json_schema_extra = {
            "example":{
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "Gustavo",
                "last_name": "Romero",
                "email": "example@example.com"
            }
        }