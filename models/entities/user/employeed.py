from typing import Optional
import uuid
from sqlmodel import Column, Field, String
from sqlmodel import Field, Relationship
from models.entities.base.base_entity import BaseEntity
from models.entities.user.person import Person
from models.entities.user.role import Role
from domain.security import get_password_hash


class Employeed(BaseEntity, table=True):
    person_id: uuid.UUID = Field(foreign_key="person.id")
    role_id: uuid.UUID = Field(foreign_key="role.id")
    username: str = Field(sa_column=Column(String(50), unique=True))
    password_hash: str = Field(sa_column=Column(String(255)))
    
    persons: Optional["Person"] = Relationship(back_populates="employeeds")
    roles: Optional["Role"] = Relationship(back_populates="employeeds")
    
    def set_password(self, password: str):
        self.password_hash = get_password_hash(password)