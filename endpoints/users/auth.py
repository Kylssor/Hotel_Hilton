from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from domain.utils.dependencies import get_db_context
from domain.service.authentication_service import AuthenticationService
from models.repository.unit_of_work import UnitOfWork
from schemas.authentication.sign_in_employeed_schema import SignInEmployeedSchema
from schemas.authentication.sign_in_customer_schema import SignInCustomerSchema
from schemas.authentication.token_schema import TokenSchema
from schemas.user.user_schemas import UserCreateSchema

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@auth_router.post("/signin/employee", response_model=TokenSchema)
async def sign_in_employee(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db=Depends(get_db_context)
):
    uow = UnitOfWork(db)
    try:
        sign_in_data = SignInEmployeedSchema(
            user_name=form_data.username,
            password=form_data.password
        )
        service = AuthenticationService(uow)
        token = service.sign_in_employee(sign_in_data)
        return TokenSchema(access_token=token)
    except Exception as e:
        uow.rollback()
        raise e
    finally:
        uow.close()

@auth_router.post("/signin/customer", response_model=TokenSchema)
async def sign_in_customer(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db=Depends(get_db_context)
):
    uow = UnitOfWork(db)
    try:
        sign_in_data = SignInCustomerSchema(
            email=form_data.username,
            password=form_data.password
        )
        service = AuthenticationService(uow)
        token = service.sign_in_customer(sign_in_data)
        return TokenSchema(access_token=token)
    except Exception as e:
        uow.rollback()
        raise e
    finally:
        uow.close()

@auth_router.post("/signup/customer")
async def signup_customer(user_data: UserCreateSchema, db=Depends(get_db_context)):
    uow = UnitOfWork(db)
    try:
        service = AuthenticationService(uow)
        service.register_customer(user_data)
        uow.commit()
        return {"message": "Cliente registrado exitosamente"}
    except Exception as e:
        uow.rollback()
        raise e
    finally:
        uow.close()

@auth_router.post("/signup/employee")
async def signup_employee(user_data: UserCreateSchema, db=Depends(get_db_context)):
    uow = UnitOfWork(db)
    try:
        service = AuthenticationService(uow)
        service.register_employee(user_data)
        uow.commit()
        return {"message": "Empleado registrado exitosamente"}
    except Exception as e:
        uow.rollback()
        raise e
    finally:
        uow.close()
