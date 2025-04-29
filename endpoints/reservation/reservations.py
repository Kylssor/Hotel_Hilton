from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Annotated, List
import uuid
from datetime import date

from domain.service.reservation_service import ReservationService
from exceptions.unauthorized_exception import UnauthorizedException
from models.repository.unit_of_work import UnitOfWork
from models.context.persistence_context import PersistenceContext
from domain.utils.dependencies import get_db_context

from domain.utils.security import validate_token_customer, validate_token_employee
from config.project_config import ProjectConfig
from models.repository.generic_repository import GenericRepository
from models.entities.user.employeed import Employeed
from models.entities.user.customer import Customer
from schemas.reservations.reservation_schema import ReservationCreate, ReservationRead

router = APIRouter(prefix="/reservations", tags=["Reservations"])

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

@router.post("/", response_model=ReservationRead)
def create_reservation(
    reservation_data: ReservationCreate,
    db_context: PersistenceContext = Depends(get_db_context),
    current_user: dict = Depends(get_current_user_from_token)
):
    uow = UnitOfWork(db_context)
    try:
        service = ReservationService(uow)
        result = service.create_reservation(reservation_data)
        uow.commit()

        reservation_response = ReservationRead(
            id=result.id,
            room_id=result.room_id,
            customer_id=result.customer_id,
            check_in_date=result.check_in_date,
            check_out_date=result.check_out_date,
            status_id=result.status_id,
            reservation_number=result.reservation_number,
        )
        return reservation_response

    except Exception as e:
        uow.rollback()
        raise e
    finally:
        uow.close()

@router.get("/customer/{customer_id}", response_model=List[ReservationRead])
def get_customer_reservations(
    customer_id: uuid.UUID,
    upcoming: bool = Query(False),
    history: bool = Query(False),
    db_context: PersistenceContext = Depends(get_db_context),
    current_user: dict = Depends(get_current_user_from_token)
):
    if current_user["id"] != customer_id and current_user["role"] not in ["SuperAdmin", "Admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")

    uow = UnitOfWork(db_context)
    try:
        service = ReservationService(uow)
        return service.get_customer_reservations(customer_id, upcoming=upcoming, history=history)
    except Exception as e:
        uow.rollback()
        raise e
    finally:
        uow.close()

@router.get("/admin", response_model=List[ReservationRead])
def get_all_reservations(
    db_context: PersistenceContext = Depends(get_db_context),
    current_user: dict = Depends(get_current_user_from_token)
):
    if current_user["role"] not in ["SuperAdmin", "Admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")

    uow = UnitOfWork(db_context)
    try:
        service = ReservationService(uow)
        return service.get_all_reservations()
    except Exception as e:
        uow.rollback()
        raise e
    finally:
        uow.close()
