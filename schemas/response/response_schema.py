from pydantic import BaseModel, Field


class ResponseSchema(BaseModel):
    message: str =  Field(default=None, nullable=False)
    
    class Config:
        json_schema_extra = {
            "example":{
                "message": "Ok",
            }
        }