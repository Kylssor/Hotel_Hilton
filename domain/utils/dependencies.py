from domain.utils.app_context import app_context
from models.context.persistence_context import PersistenceContext

# Obtener el contexto de base de datos
def get_db_context() -> PersistenceContext:
    return app_context.db_context

