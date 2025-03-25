from typing import Optional
import uuid
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship
from models.entities.base.base_entity import BaseEntity
from models.entities.user.person import Person


class Customer(BaseEntity, table=True):
    person_id: uuid.UUID = Field(foreign_key="person.id")
    password_hash: str = Field(sa_column=Column(String(255)))

    person: Optional["Person"] = Relationship(back_populates="customers")