from domain.utils import argument_validator
from domain.utils.list_helper import first_or_none
from domain.utils.security import create_access_jwt_token, verify_password  # ⬅️ quitado hash_sha256
from exceptions.unauthorized_exception import UnauthorizedException
from models.entities.user.employeed import Employeed
from models.entities.user.customer import Customer
from models.entities.user.person import Person
from models.repository.generic_repository import GenericRepository
from models.repository.unit_of_work import UnitOfWork
from schemas.authentication.sign_in_employeed_schema import SignInEmployeedSchema
from schemas.authentication.sign_in_customer_schema import SignInCustomerSchema


class AuthenticationService():
    def __init__(self, uow: UnitOfWork):
        self.employeed_repo = GenericRepository(uow.session, Employeed)
        self.customer_repo = GenericRepository(uow.session, Customer)

    def sign_in_emploty(self, sing_in_data: SignInEmployeedSchema) -> str:
        argument_validator.validate_empty(sing_in_data.user_name, "El nombre de usuario no puede estar vacío")

        employeed: Employeed = first_or_none(
            self.employeed_repo.read_by_options(
                Employeed.user_name == sing_in_data.user_name
            )
        )

        if not employeed:
            raise UnauthorizedException("El usuario proporcionado no está asociado con ninguna cuenta registrada. Por favor, verifique su nombre de usuario")

        if not verify_password(sing_in_data.password, employeed.password_hash):
            raise UnauthorizedException("La contraseña proporcionada es incorrecta. Por favor, inténtelo de nuevo.")

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
            raise UnauthorizedException("No se encontró un cliente con ese correo electrónico proporcionado, verifique si está correcto.")

        if not verify_password(sign_in_data.password, customer.password_hash):
            raise UnauthorizedException("La contraseña proporcionada es incorrecta. Por favor, inténtelo de nuevo.")

        data = {
            "id": str(customer.id),
            "tipo_usuario": "cliente"
        }

        return create_access_jwt_token(data)

