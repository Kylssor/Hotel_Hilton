from models.entities.reservation.reservationstatus import ReservationStatus
from models.repository.generic_repository import GenericRepository
from models.repository.unit_of_work import UnitOfWork
import uuid


def create(uow: UnitOfWork):
    status_repo = GenericRepository(uow.session, ReservationStatus)

    # Si ya hay estados, no hacer nada
    if status_repo.read_by_options():
        return

    statuses = [
        ReservationStatus(
            id=uuid.uuid4(),
            name="Pendiente",
            description="Reserva creada pero aún no confirmada"
        ),
        ReservationStatus(
            id=uuid.uuid4(),
            name="Confirmada",
            description="Reserva confirmada y activa"
        ),
        ReservationStatus(
            id=uuid.uuid4(),
            name="Cancelada",
            description="Reserva cancelada por el cliente o sistema"
        )
    ]

    status_repo.add_all(statuses)
    uow.session.flush()
