from sqlalchemy.orm import Session
from context.persistence_context import PersistenceContext

class UnitOfWork:
    def __init__(self, db_context: PersistenceContext):
        self._db_context = db_context
        self.session: Session = self._db_context._session_factory()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def close(self):
        self.session.close()