from pydantic import BaseModel, Field


class SignInEmployeedSchema(BaseModel):
    user_name: str = Field(..., max_length=100)
    password: str = Field(...)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@hotel.com",
                "password": "contraseña_segura"
            }
        }