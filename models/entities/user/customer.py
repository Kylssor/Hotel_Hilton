from typing import Optional
import uuid
from sqlmodel import Field, Relationship
from models.entities.base.Base_entity import BaseEntity
from models.entities.user.person import Person


class Customer(BaseEntity, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    person_id: uuid.UUID = Field(foreign_key="person.id")
 
   
    persons: Optional["Person"] = Relationship(back_populates="customers")