from typing import TYPE_CHECKING, Optional
import uuid
from sqlmodel import Field, Relationship, Column, String
from models.entities.base.base_entity import BaseEntity


if TYPE_CHECKING:
    from models.entities.location.city import City
    from models.entities.room.room import Room


class Location(BaseEntity, table=True):
    name: str = Field(sa_column=Column("name", String(100), unique=True))
    address: str = Field(sa_column=Column("address", String(200)))
    phone: str = Field(sa_column=Column("phone", String(15)))
    city_id: uuid.UUID = Field(foreign_key="city.id")

    city: Optional["City"] = Relationship()
    rooms: list["Room"] = Relationship(back_populates="location")