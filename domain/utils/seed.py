
from models.context.persistence_context import PersistenceContext
from models.repository.unit_of_work import UnitOfWork
from models.seed import (
    initializer_countrys_citys,
    initializer_employeed,
    initializer_roles,
    initializer_locations_rooms,
    initializer_reservation_status,
    initializer_roomstatus,
    initializer_roomtype,
)

def run_seed(db_context: PersistenceContext):
    uow = UnitOfWork(db_context)

    try:
        initializer_countrys_citys.create(uow)
        initializer_roles.create(uow)
        initializer_employeed.create(uow)
        initializer_roomtype.create(uow)
        initializer_roomstatus.create(uow)
        initializer_locations_rooms.create(uow)
        initializer_reservation_status.create(uow)
        

        uow.commit()
        print("Todas las semillas insertadas correctamente.")
    except Exception as e:
        uow.rollback()
        print(f"Error en la carga de seeds: {e}")
        raise e 
    finally:
        uow.close()