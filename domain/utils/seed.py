
from models.context.persistence_context import PersistenceContext
from models.repository.unit_of_work import UnitOfWork
from models.seed import initializer_countrys_citys, initializer_employeed, initializer_roles


def run_seed(db_context: PersistenceContext):
    uow = UnitOfWork(db_context)

    try:
        initializer_roles.create(uow)
        initializer_countrys_citys.create(uow)
        initializer_employeed.create(uow)

        uow.commit()
        print("Todas las semillas insertadas correctamente.")
    except Exception as e:
        uow.rollback()
        print(f"Error en la carga de seeds: {e}")
    finally:
        uow.close()