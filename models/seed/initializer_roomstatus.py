from models.entities.room.room import RoomStatus
from models.repository.generic_repository import GenericRepository
from models.repository.unit_of_work import UnitOfWork
import uuid

def create(uow: UnitOfWork):
    repo = GenericRepository(uow.session, RoomStatus)

    if repo.read_by_options():
        return

    estados = [
        RoomStatus(id=uuid.uuid4(), name="Disponible", description="Habitación disponible para reserva"),
        RoomStatus(id=uuid.uuid4(), name="Ocupada", description="Habitación actualmente ocupada"),
        RoomStatus(id=uuid.uuid4(), name="Mantenimiento", description="Habitación en proceso de mantenimiento")
    ]

    repo.add_all(estados)
    uow.session.flush()
