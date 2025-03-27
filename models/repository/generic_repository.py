import uuid
from exceptions.duplicated_error_exception import DuplicatedErrorException
from exceptions.not_found_error_exception import NotFoundErrorException
from models.entities.base.base_entity import BaseEntity
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from typing import Callable, TypeVar, Generic

from models.context.persistence_context import PersistenceContext

Entity = TypeVar("Entity", bound=BaseEntity)

class GenericRepository(Generic[Entity]):

    def __init__(self, session: Session, entity: type[Entity]) -> None:
        self.session =  session
        self.entity = entity

    def read_by_options(self, 
        *criterion: Callable[[type[Entity]], bool],
        include_propiertys: str = str()
    ):
        query = self.session.query(self.entity)
        if len(include_propiertys) != 0:
            for propierty in include_propiertys.split(","):
                query = query.options(joinedload(getattr(self.entity, propierty)))

        # Validar que los filtros no involucren tablas externas sin join
        for c in criterion:
            if hasattr(c, 'table') and c.table != self.entity.__table__:
                raise ValueError("Criterios de filtrado involucran otras tablas sin un JOIN adecuado. Revisa tu uso del repositorio.")

        filtered_query = query.filter(*criterion)
        query = filtered_query.all()
        return query

    def read_by_id(self,
        id: uuid.UUID,
        include_propiertys: str = str()
    ):
        query = self.session.query(self.entity)
        if len(include_propiertys) != 0:
            for propierty in include_propiertys.split(","):
                query = query.options(joinedload(getattr(self.entity, propierty)))
        query = query.filter(self.entity.id == id).first()
        if not query:
            raise NotFoundErrorException(detail=f"not found id : {id}")
        return query

    def add(self, entity: type[Entity]):
        query = self.entity = entity
        try:
            self.session.add(query)
            self.session.flush()
        except IntegrityError as e:
            raise DuplicatedErrorException(detail=str(e.orig))
        return query

    def add_all(self, entity: list[Entity]):
        query = self.entity = entity
        try:
            self.session.add_all(query)
            self.session.flush()
        except IntegrityError as e:
            raise DuplicatedErrorException(detail=str(e.orig))
        return query

    def update(
        self,
        entity: Entity
    ):
        non_null_data = {
            attr: value for attr, value in vars(entity).items()
            if value is not None and attr != '_sa_instance_state' and attr != 'created_at'
        }

        self.session.query(self.entity).filter(self.entity.id == entity.id).update(non_null_data)
        self.session.flush()
        return self.read_by_id(entity.id)

    def delete_by_id(self, id: uuid.UUID):
        query = self.session.query(self.entity).filter(self.entity.id == id).first()
        if not query:
            raise NotFoundErrorException(detail=f"not found id : {id}")
        self.session.delete(query)
        self.session.flush()

    def delete_by_options(self, 
        *criterion: Callable[[type[Entity]], bool]
    ):
        query = self.session.query(self.entity)

        # Validar que los filtros no involucren tablas externas sin join
        for c in criterion:
            if hasattr(c, 'table') and c.table != self.entity.__table__:
                raise ValueError("Criterios de borrado involucran otras tablas sin un JOIN adecuado. Revisa tu uso del repositorio.")

        filtered_query = query.filter(*criterion)
        query = filtered_query.all()
        if query:
            for item in query:
                self.session.delete(item)
                self.session.flush()
