from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from domain.utils.dependencies import get_db_context
from domain.service.authentication_service import AuthenticationService
from models.repository.unit_of_work import UnitOfWork
from schemas.authentication.sign_in_employeed_schema import SignInEmployeedSchema
from schemas.authentication.token_schema import TokenSchema
from schemas.user.user_schemas import UserCreateSchema

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@auth_router.post("/signin/employee", response_model = TokenSchema)
async def sign_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db=Depends(get_db_context)
):
    uow = UnitOfWork(db)
    
    try:
        sign_in_data = SignInEmployeedSchema(
            user_name= form_data.username,
            password = form_data.password
        )

        service = AuthenticationService(uow)

        return TokenSchema(access_token=service.sign_in_emploty(sign_in_data))
    except Exception as e:
        uow.rollback()
        raise e
    finally:
        uow.close()

@auth_router.post("/signup/customer")
async def signup_customer(user_data: UserCreateSchema):
    return {"response": "Ok"}

@auth_router.post("/signup/employee")
async def signup_employee(user_data: UserCreateSchema):
    return {"response": "Ok"}
