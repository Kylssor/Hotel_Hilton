from typing import TYPE_CHECKING, Optional
import uuid
from sqlmodel import SQLModel, Field, Relationship, Column, String

if TYPE_CHECKING:
    from models.entities.room.room import Room

class RoomStatus(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(sa_column=Column("name", String(100), unique=True))
    description: Optional[str] = Field(default=None, sa_column=Column("description", String))

    rooms: list["Room"] = Relationship(back_populates="status")