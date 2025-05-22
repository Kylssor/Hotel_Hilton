from typing import Annotated
import uuid

from fastapi import Depends, HTTPException
from config.project_config import ProjectConfig
from domain.utils.app_context import app_context
from exceptions.unauthorized_exception import UnauthorizedException
from models.context.persistence_context import PersistenceContext
from models.entities.user.customer import Customer
from models.entities.user.employeed import Employeed
from models.repository.generic_repository import GenericRepository
from models.repository.unit_of_work import UnitOfWork
from domain.utils.security import validate_token_customer, validate_token_employee

# Obtener el contexto de base de datos
def get_db_context() -> PersistenceContext:
    return app_context.db_context

def get_current_user_from_token(
    token: Annotated[str, Depends(ProjectConfig.OAUTH2_SCHEME_CUSTOMER())],
    db_context: PersistenceContext = Depends(get_db_context)
):
    try:
        payload = validate_token_employee(token)
    except UnauthorizedException:
        payload = validate_token_customer(token)

    user_type = payload.get("tipo_usuario")
    user_id = payload.get("id")

    uow = UnitOfWork(db_context)
    try:
        if user_type == "empleado":
            employeed_repo = GenericRepository(uow.session, Employeed)
            employeed = employeed_repo.read_by_id(uuid.UUID(user_id), include_propiertys="roles")
            return {"id": employeed.id, "role": employeed.roles.name, "tipo_usuario": user_type}
        elif user_type == "cliente":
            customer_repo = GenericRepository(uow.session, Customer)
            customer = customer_repo.read_by_id(uuid.UUID(user_id))
            return {"id": customer.id, "role": "cliente", "tipo_usuario": user_type}
        raise HTTPException(status_code=401, detail="Token inválido")
    finally:
        uow.close()

