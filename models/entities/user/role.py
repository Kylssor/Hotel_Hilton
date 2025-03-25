from typing import List, Optional
from sqlmodel import Column, Enum, Field, Relationship, func, String, Text
from models.entities.base import base_entity
from models.entities.user.employeed import Employeed

class RoleName(str, Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"
    CUSTOMER = "customer"

class Role(base_entity, table=True):
    name: str = Field(sa_column=Column("name", String(100), unique=True))
    description: Optional[str] = Field(sa_column=Column("description", Text))
    
    employeeds: List["Employeed"] = Relationship(back_populates="roles")