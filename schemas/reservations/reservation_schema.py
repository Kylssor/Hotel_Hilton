from datetime import date
import uuid
from pydantic import BaseModel

class ReservationCreate(BaseModel):
    room_id: uuid.UUID
    customer_id: uuid.UUID
    check_in_date: date
    check_out_date: date
    status_id: uuid.UUID
    reservation_number: str

    class Config:
        json_schema_extra = {
            "example": {
                "room_id": "abc12345-6789-def0-1234-56789abcdef0",
                "customer_id": "def67890-1234-4567-890a-bcdef1234567",
                "check_in_date": "2025-05-01",
                "check_out_date": "2025-05-05",
                "status_id": "aaa11111-2222-3333-4444-555566667777",
                "reservation_number": "RES-2025-0001"
            }
        }


class ReservationRead(BaseModel):
    id: uuid.UUID
    room_id: uuid.UUID
    customer_id: uuid.UUID
    check_in_date: date
    check_out_date: date
    status_id: uuid.UUID
    reservation_number: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "cba98765-4321-fedc-9876-543210fedcba",
                "room_id": "abc12345-6789-def0-1234-56789abcdef0",
                "customer_id": "def67890-1234-4567-890a-bcdef1234567",
                "check_in_date": "2025-05-01",
                "check_out_date": "2025-05-05",
                "status_id": "aaa11111-2222-3333-4444-555566667777",
                "reservation_number": "RES-2025-0001"
            }
        }
