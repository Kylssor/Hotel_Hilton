from datetime import date
from typing import TYPE_CHECKING, Optional
import uuid
from sqlmodel import Column, Field, Relationship, SQLModel, String

if TYPE_CHECKING:
    from models.entities.room.room import Room


class Reservation(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    room_id: uuid.UUID = Field(foreign_key="room.id")
    customer_id: uuid.UUID = Field(foreign_key="customer.id")
    check_in_date: date
    check_out_date: date
    status_id: uuid.UUID = Field(foreign_key="reservationstatus.id")
    reservation_number: str = Field(sa_column=Column("reservation_number", String(20), unique=True))

    rooms: Optional["Room"] = Relationship(back_populates="reservations")