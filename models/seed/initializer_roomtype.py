from models.entities.room.room import RoomType
from models.repository.generic_repository import GenericRepository
from models.repository.unit_of_work import UnitOfWork
import uuid

def create(uow: UnitOfWork):
    repo = GenericRepository(uow.session, RoomType)

    if repo.read_by_options():
        return

    tipos = [
        "Estándar",
        "Suite",
        "Familiar",
        "Ejecutiva",
        "Lujo",
        "Con vista",
        "Doble",
        "Individual",
        "Matrimonial",
        "Superior"
    ]

    result = [RoomType(id=uuid.uuid4(), name=tipo, description=f"Habitación tipo {tipo}") for tipo in tipos]

    repo.add_all(result)
    uow.session.flush()

