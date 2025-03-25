from typing import Optional
import uuid
from datetime import datetime
from sqlmodel import Column, DateTime, Field, func, String
from models.entities.base.Base_entity import BaseEntity
from sqlmodel import Field, Relationship
from models.entities.base import BaseEntity
from models.entities.user.person import Person
from models.entities.user.role import Role
from core.security import get_password_hash


class Employeed(BaseEntity, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    person_id: uuid.UUID = Field(foreign_key="person.id")
    role_id: uuid.UUID = Field(foreign_key="role.id")
    username: str = Field(sa_column=Column(String(50), unique=True))
    password_hash: str = Field(sa_column=Column(String(255)))
    
    persons: Optional["Person"] = Relationship(back_populates="employeeds")
    roles: Role = Relationship(back_populates="employeeds")
    
    def set_password(self, password: str):
        self.password_hash = get_password_hash(password)