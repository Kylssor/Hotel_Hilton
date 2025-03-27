from typing import TYPE_CHECKING, List
from sqlmodel import Column, Field, Relationship, String
from models.entities.base.base_entity import BaseEntity


if TYPE_CHECKING:
    from models.entities.user.employeed import Employeed
    from models.entities.user.customer import Customer

class Role(BaseEntity, table=True):
    name: str = Field(sa_column=Column("name", String(100), unique=True))
    
    employeeds: list["Employeed"] = Relationship(back_populates="roles")
    customers: list["Customer"] = Relationship(back_populates="roles")