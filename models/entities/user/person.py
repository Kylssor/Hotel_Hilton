from typing import TYPE_CHECKING, Optional
from datetime import datetime
import uuid
from sqlmodel import Column, DateTime, Field, Relationship, func, String
from models.entities.base.base_entity import BaseEntity
from models.entities.location.city import City

if TYPE_CHECKING:
    from models.entities.user.customer import Customer
    from models.entities.user.employeed import Employeed


class Person(BaseEntity, table=True):
    identification_number: str = Field(sa_column=Column(String(20), unique=True))
    first_name: str = Field(sa_column=Column(String(100)))
    last_name: str = Field(sa_column=Column(String(100)))
    email: str = Field(sa_column=Column(String(100), unique=True))
    phone: str = Field(sa_column=Column(String(15)))
    address: str = Field(sa_column=Column(String(200)))
    city_id: uuid.UUID = Field(foreign_key="city.id")

    city: Optional["City"] = Relationship(back_populates="persons")
    customers: list["Customer"] = Relationship(back_populates="persons")
    employeeds: list["Employeed"] = Relationship(back_populates="persons")