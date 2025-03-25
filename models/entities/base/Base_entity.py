from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel, func

class BaseEntity(SQLModel):
    model_config = {"arbitrary_types_allowed": True}

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True
    )
    created_at: datetime = Field(
        default=func.now(),
        sa_column=Column(DateTime(timezone=True))  # Sin comas extras
    )
    updated_at: datetime = Field(
        default=func.now(),
        sa_column=Column(
            DateTime(timezone=True),
            onupdate=func.now()  # onupdate se define aquí
        )
    )