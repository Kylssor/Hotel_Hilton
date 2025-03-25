from models.entities.user.role import Role
from models.repository.generic_repository import GenericRepository
from models.repository.unit_of_work import UnitOfWork


def create(uow: UnitOfWork):
    role_repo = GenericRepository(uow.session, Role)
    
    count: int = role_repo.read_by_options().count()
    
    if count == 0:
        return
    
    roles = list[
        Role(
            name="SuperAdmin"
        ),
        Role(
            name="Admin"
        ),
        Role(
            name="Recepcionista"
        )
    ]
    
    role_repo.add_all(roles)