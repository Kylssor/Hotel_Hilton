from sqlalchemy import select
from domain.utils import argument_validator
from domain.utils.list_helper import first_or_none
from domain.utils.security import create_access_jwt_token, verify_password, get_password_hash
from exceptions.unauthorized_exception import UnauthorizedException
from models.entities.user.employeed import Employeed
from models.entities.user.customer import Customer
from models.entities.user.person import Person
from models.entities.user import role
from models.repository.generic_repository import GenericRepository
from models.repository.unit_of_work import UnitOfWork
from schemas.authentication.sign_in_employeed_schema import SignInEmployeedSchema
from schemas.authentication.sign_in_customer_schema import SignInCustomerSchema
from schemas.user.user_schemas import UserCreateSchema


class AuthenticationService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.session = uow.session
        self.employeed_repo = GenericRepository(self.session, Employeed)
        self.customer_repo = GenericRepository(self.session, Customer)

    def sign_in_employee(self, sign_in_data: SignInEmployeedSchema) -> str:
        argument_validator.validate_empty(sign_in_data.user_name, "El nombre de usuario no puede estar vacío")

        employeed: Employeed = first_or_none(
            self.employeed_repo.read_by_options(
                Employeed.user_name == sign_in_data.user_name
            )
        )

        if not employeed:
            raise UnauthorizedException("El usuario no está registrado. Verifique el nombre de usuario.")

        if not verify_password(sign_in_data.password, employeed.password_hash):
            raise UnauthorizedException("Contraseña incorrecta.")

        data = {
            "id": str(employeed.id),
            "tipo_usuario": "empleado"
        }
        return create_access_jwt_token(data)

    def sign_in_customer(self, sign_in_data: SignInCustomerSchema) -> str:
        argument_validator.validate_empty(sign_in_data.email, "El correo no puede estar vacío")

        customer: Customer = first_or_none(
            self.customer_repo.read_by_options(
                Person.email == sign_in_data.email,
                include_propiertys="person"
            )
        )

        if not customer:
            raise UnauthorizedException("Correo no registrado como cliente.")

        if not verify_password(sign_in_data.password, customer.password_hash):
            raise UnauthorizedException("Contraseña incorrecta.")

        data = {
            "id": str(customer.id),
            "tipo_usuario": "cliente"
        }
        return create_access_jwt_token(data)

    def register_customer(self, user_data: UserCreateSchema):
        existing_person = self.session.execute(
            select(Person).where(Person.email == user_data.email)
        ).scalar_one_or_none()

        if existing_person:
            raise ValueError("Ya existe una persona registrada con este correo.")

        new_person = Person(
            identification_number=user_data.identification_number,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            phone=user_data.phone,
            address=user_data.address,
            city_id=user_data.city_id
        )
        self.session.add(new_person)
        self.session.flush()

        cliente_role = self.session.execute(
            select(role).where(role.name == "Cliente")
        ).scalar_one_or_none()

        if not cliente_role:
            raise ValueError("Rol 'Cliente' no encontrado.")

        new_customer = Customer(
            person_id=new_person.id,
            role_id=cliente_role.id,
            password_hash=get_password_hash(user_data.password)
        )
        self.session.add(new_customer)

    def register_employee(self, user_data: UserCreateSchema):
        existing = self.session.execute(
            select(Person)
            .where(Person.first_name == user_data.first_name)
            .where(Person.last_name == user_data.last_name)
            .join(Employeed)
        ).scalar_one_or_none()

        if existing:
            raise ValueError("Ya existe un empleado con ese nombre y apellido.")

        new_person = Person(
            identification_number=user_data.identification_number,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            phone=user_data.phone,
            address=user_data.address,
            city_id=user_data.city_id
        )
        self.session.add(new_person)
        self.session.flush()

        employeed_role = self.session.execute(
            select(role).where(role.name == "Empleado")
        ).scalar_one_or_none()

        if not employeed_role:
            raise ValueError("Rol 'Empleado' no encontrado.")

        new_employeed = Employeed(
            person_id=new_person.id,
            role_id=employeed_role.id,
            user_name=user_data.email,
            password_hash=get_password_hash(user_data.password)
        )
        self.session.add(new_employeed)
