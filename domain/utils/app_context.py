from models.context.persistence_context import PersistenceContext

class AppContext:
    db_context: PersistenceContext = None

app_context = AppContext()