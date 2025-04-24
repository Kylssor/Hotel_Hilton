from datetime import datetime
import uuid
from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel, func

class BaseEntity(SQLModel):
    id: uuid.UUID = Field(primary_key=True)
    created_at: datetime = Field(sa_type=DateTime(timezone=True), default=func.now())
    updated_at: datetime = Field(sa_type=DateTime(timezone=True), default=func.now(),sa_column_kwargs={"onupdate": func.now(), "nullable": True})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = uuid.uuid4()
