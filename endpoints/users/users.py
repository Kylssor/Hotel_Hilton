from fastapi import APIRouter
from schemas.user.user_schemas import UserCreateSchema, UserResponseSchema
from models.entities.user.person import Person
from models.entities.user.customer import Customer
from domain.utils.security import get_password_hash

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)
