from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from models.entities.user.person import Person
from schemas.authentication.sign_in_schema import SignInSchema
from schemas.authentication.token_schema import TokenSchema
from models.entities.user.employeed import Employeed
from models.entities.user.customer import Customer
from domain.utils.security import verify_password, create_access_token

router = APIRouter(tags=["Autenticación"])

