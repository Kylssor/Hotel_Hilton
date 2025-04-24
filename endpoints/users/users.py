# routers/users.py
from typing import Annotated
from fastapi import APIRouter, Depends
from config.project_config import ProjectConfig
from domain.service.user_service import UserService
from domain.utils.dependencies import get_db_context
from models.repository.unit_of_work import UnitOfWork
from domain.utils.security import validate_token_customer, validate_token_employee
from schemas.user.user_schemas import EmployeedResponseSchema, UserResponseSchema

router = APIRouter(prefix="/user", tags=["Users"])

@router.get("/customer/profile", response_model=UserResponseSchema)
async def get_customer_profile(
    token: Annotated[str, Depends(ProjectConfig.OAUTH2_SCHEME_CUSTOMER())],
    db=Depends(get_db_context)
):
    usuario = validate_token_customer(token)
    uow = UnitOfWork(db)
    user_service = UserService(uow)
    return user_service.get_customer_profile(usuario)


@router.get("/employeed/profile", response_model=EmployeedResponseSchema)
async def get_employee_profile(
    token: Annotated[str, Depends(ProjectConfig.OAUTH2_SCHEME_CUSTOMER())],
    db=Depends(get_db_context)
):
    usuario = validate_token_employee(token)
    uow = UnitOfWork(db)
    user_service = UserService(uow)
    return user_service.get_employee_profile(usuario)


@router.get("/employeed/role")
async def get_role(
    token: Annotated[str, Depends(ProjectConfig.OAUTH2_SCHEME_EMPLOYEED())],
    db=Depends(get_db_context)
):
    validate_token_employee(token)
    uow = UnitOfWork(db)
    user_service = UserService(uow)
    return user_service.get_employee_roles()


