from typing import Optional
import uuid
from datetime import date
from sqlmodel import SQLModel, Field, Relationship, Column, String
from sqlalchemy import DECIMAL
from pydantic import BaseModel

class ReservationStatus(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(sa_column=Column("name", String(100), unique=True))
    description: Optional[str] = Field(default=None, sa_column=Column("description", String))