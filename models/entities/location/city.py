from typing import TYPE_CHECKING, Optional
import uuid
from sqlmodel import Column, Field, Relationship, String
from models.entities.base.base_entity import BaseEntity
from models.entities.location.country import Country

if TYPE_CHECKING:
    from models.entities.user.person import Person


class City(BaseEntity, table=True):
    name: str = Field(sa_column=Column("name", String(100)))
    country_id: uuid.UUID = Field(foreign_key="country.id")
    
    country: Optional["Country"] = Relationship(back_populates="cities")
    persons: list["Person"] = Relationship(back_populates="city")