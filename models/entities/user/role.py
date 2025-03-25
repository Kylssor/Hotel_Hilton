from typing import TYPE_CHECKING
from sqlmodel import Column, Field, Relationship, String
from models.entities.base.base_entity import BaseEntity

if TYPE_CHECKING:
    from models.entities.user.employeed import Employeed

class Role(BaseEntity, table=True):
    name: str = Field(sa_column=Column("name", String(100), unique=True))
    
    employeeds: list["Employeed"] = Relationship(back_populates="role")