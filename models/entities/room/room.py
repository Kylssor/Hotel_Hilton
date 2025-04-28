from sqlmodel import Field, Relationship, Column, String, DECIMAL
from typing import TYPE_CHECKING, Optional
import uuid
from models.entities.base.base_entity import BaseEntity
from models.entities.room.roomtype import RoomType
from models.entities.room.roomstatus import RoomStatus
from models.entities.location.location import Location
from models.entities.reservation.reservation import Reservation

class Room(BaseEntity, table=True):
    number: str = Field(sa_column=Column("number", String(10), unique=True))
    type_id: uuid.UUID = Field(foreign_key="roomtype.id")
    status_id: uuid.UUID = Field(foreign_key="roomstatus.id")
    price_per_night: float = Field(sa_column=Column("price_per_night", DECIMAL(10, 2)))
    size: float = Field(sa_column=Column("size", DECIMAL(10, 2)))
    description: Optional[str] = Field(default=None, sa_column=Column("description", String))
    tax: float = Field(sa_column=Column("tax", DECIMAL(5, 2)))
    image_url: Optional[str] = Field(default=None, sa_column=Column("image_url", String(255)))
    location_id: uuid.UUID = Field(foreign_key="location.id")

    type: Optional[RoomType] = Relationship(back_populates="rooms")
    status: Optional[RoomStatus] = Relationship(back_populates="rooms")
    location: Optional[Location] = Relationship(back_populates="rooms")
    reservations: list[Reservation] = Relationship(back_populates="room")