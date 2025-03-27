from typing import List, Optional
import uuid
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship
from models.entities.base.base_entity import BaseEntity
from models.entities.user.person import Person
from models.entities.user.role import Role


class Customer(BaseEntity, table=True):
    person_id: uuid.UUID = Field(foreign_key="person.id")
    role_id: uuid.UUID = Field(foreign_key="role.id")
    password_hash: str = Field(sa_column=Column(String(255)))

    persons: Optional["Person"] = Relationship(back_populates="customers")
    roles: Optional["Role"] = Relationship(back_populates="customers")