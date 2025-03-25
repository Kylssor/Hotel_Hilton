from typing import Optional
import uuid
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship
from domain.security import get_password_hash
from models.entities.base.base_entity import BaseEntity
from models.entities.user.person import Person


class Customer(BaseEntity, table=True):
    person_id: uuid.UUID = Field(foreign_key="person.id")
    password_hash: str = Field(sa_column=Column(String(255)))

    persons: Optional["Person"] = Relationship(back_populates="customers")
    
    def set_password(self, password: str):
        self.password_hash = get_password_hash(password)