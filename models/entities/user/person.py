from typing import List
from datetime import datetime
import uuid
from sqlmodel import Column, DateTime, Field, Relationship, func, String, Text
from models.entities.base.Base_entity import BaseEntity
from models.entities.user.customer import Customer
from models.entities.user.employeed import Employeed


class Person(BaseEntity, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    identification_num: str = Field(sa_column=Column(String(100), unique=True))
    first_name: str = Field(sa_column=Column(String(100)))
    last_name: str = Field(sa_column=Column(String(100)))
    email: str = Field(sa_column=Column(String(255), unique=True))
    phone: str = Field(sa_column=Column(String(15)))
    address: str = Field(sa_column=Column(String(300)))
    registration_date: datetime = Field(default=func.now(), sa_type=DateTime(timezone=True))
    

customers: List["Customer"] = Relationship(back_populates="persons")
employeeds: List["Employeed"] = Relationship(back_populates="persons")