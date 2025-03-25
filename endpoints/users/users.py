from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from domain.dependencies import get_current_user
from schemas.user.user_schemas import UserCreateSchema, UserResponseSchema
from models.entities.user.person import Person
from models.entities.user.customer import Customer
from domain.utils.security import get_password_hash

router = APIRouter(tags=["Usuarios"])

@router.post("/signup/customer", response_model=UserResponseSchema)
async def signup_customer(user_data: UserCreateSchema):
    return {"response": "Ok"}

@router.post("/signup/employee", response_model=UserResponseSchema)
async def signup_employee(user_data: UserCreateSchema):
    return {"response": "Ok"}