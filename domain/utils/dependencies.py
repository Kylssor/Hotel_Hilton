from models.context.persistence_context import PersistenceContext
from main import app_creator

def get_db_context() -> PersistenceContext:
    return app_creator.db_context