from models.context.persistence_context import PersistenceContext
from domain.utils.app_context import app_context

def get_db_context() -> PersistenceContext:
    return app_context.db_context