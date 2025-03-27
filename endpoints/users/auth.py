from sqlalchemy import select
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from domain.utils.dependencies import get_db_context
from domain.service.authentication_service import AuthenticationService
from domain.utils.security import get_password_hash
from models.entities.user.customer import Customer
from models.entities.user.employeed import Employeed
from models.entities.user.person import Person
from models.repository.unit_of_work import UnitOfWork
from schemas.authentication.sign_in_employeed_schema import SignInEmployeedSchema
from schemas.authentication.sign_in_customer_schema import SignInCustomerSchema
from schemas.authentication.token_schema import TokenSchema
from schemas.user.user_schemas import UserCreateSchema

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@auth_router.post("/signin/employee", response_model = TokenSchema)
async def sign_in_employee(
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
        
        
@auth_router.post("/signin/customer", response_model = TokenSchema)
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

        return TokenSchema(access_token=service.sign_in_customer(sign_in_data))
    except Exception as e:
        uow.rollback()
        raise e
    finally:
        uow.close()

@auth_router.post("/signup/customer")
async def signup_customer(user_data: UserCreateSchema, db=Depends(get_db_context)):
    uow = UnitOfWork(db)

    try:
        session = uow.session

        # Validar que el correo no esté registrado
        query = select(Person).where(Person.email == user_data.email)
        existing_person = session.execute(query).scalar_one_or_none()


        if existing_person:
            raise ValueError("Ya existe una persona registrada con este correo.")

        # Crear la persona
        new_person = Person(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            phone=user_data.phone,
            address=user_data.address,
            city_id=user_data.city_id
        )

        session.add(new_person)
        session.flush() 

        # Crear el cliente
        new_customer = Customer(
            person_id=new_person.id,
            password_hash=get_password_hash(user_data.password)
        )

        session.add(new_customer)
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
        session = uow.session

        # Validar que no exista ya un empleado con ese nombre + apellido
        query = (
            select(Person)
            .where(Person.first_name == user_data.first_name)
            .where(Person.last_name == user_data.last_name)
            .join(Employeed)
        )
        existing = session.execute(query).scalar_one_or_none()

        if existing:
            raise ValueError("Ya existe un empleado con el mismo nombre y apellido.")

        # Crear la persona
        new_person = Person(
            identification_number=user_data.identification_number,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            phone=user_data.phone,
            address=user_data.address,
            city_id=user_data.city_id
        )
        session.add(new_person)
        session.flush()  # obtiene new_person.id

        # Crear el empleado
        new_employeed = Employeed(
            person_id=new_person.id,
            role_id=None,  # ← puedes asignar un role_id si ya tienes uno por defecto
            user_name=user_data.email,  # o podrías pedir username aparte si quieres
            password_hash=get_password_hash(user_data.password)
        )
        session.add(new_employeed)

        uow.commit()
        return {"message": "Empleado registrado exitosamente"}

    except Exception as e:
        uow.rollback()
        raise e
    finally:
        uow.close()
