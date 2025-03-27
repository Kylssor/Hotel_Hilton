from typing import Optional
import uuid
from sqlmodel import Column, Field, String, Relationship
from models.entities.base.base_entity import BaseEntity
from models.entities.user.person import Person
from models.entities.user.role import Role


class Employeed(BaseEntity, table=True):
    person_id: uuid.UUID = Field(foreign_key="person.id")
    role_id: uuid.UUID = Field(foreign_key="role.id")
    user_name: str = Field(sa_column=Column(String(50), unique=True))
    password_hash: str = Field(sa_column=Column(String(255)))
    
    persons: Optional["Person"] = Relationship(back_populates="employeeds")
    roles: Optional["Role"] = Relationship(back_populates="employeeds")