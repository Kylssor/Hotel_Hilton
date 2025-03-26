from fastapi import security
from domain.utils import argument_validator
from domain.utils.list_helper import first_or_none
from domain.utils.security import create_access_jwt_token, hash_sha256, verify_password
from exceptions.unauthorized_exception import UnauthorizedException
from models.entities.user.employeed import Employeed
from models.repository.generic_repository import GenericRepository
from models.repository.unit_of_work import UnitOfWork
from schemas.authentication.sign_in_employeed_schema import SignInEmployeedSchema


class AuthenticationService():
    def __init__(self, uow: UnitOfWork):
        self.employeed_repo = GenericRepository(uow.session, Employeed)
    
    def sign_in_emploty(self, sing_in_data: SignInEmployeedSchema)-> str:
        argument_validator.validate_empty(sing_in_data.user_name, "El nombre de usuario no puede estar vacio")
        
        employeed: Employeed = first_or_none(
            self.employeed_repo.read_by_options(
                Employeed.user_name == sing_in_data.user_name
            )
        )

        if not employeed:
            raise UnauthorizedException("El usuario proporcionado no está asociado con ninguna cuenta registrada. Por favor, verifique su nombre de usuario")

        if not verify_password(sing_in_data.password, employeed.password_hash):
            raise UnauthorizedException("La contraseña proporcionada es incorrecta. Por favor, inténtelo de nuevo.")

        data={"id": str(employeed.id)}
        
        return create_access_jwt_token(data)