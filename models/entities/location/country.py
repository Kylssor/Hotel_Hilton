from typing import TYPE_CHECKING
from sqlmodel import Column, Field, Relationship, String
from models.entities.base.base_entity import BaseEntity

if TYPE_CHECKING:
    from models.entities.location.city import City


class Country(BaseEntity, table=True):
    name: str = Field(sa_column=Column("name", String(100)))
    iso_code: str = Field(sa_column=Column("iso_code", String(100)))
    
    cities: list["City"] = Relationship(back_populates="country")