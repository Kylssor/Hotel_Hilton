import uuid
from models.entities.room.room import Room
from schemas.room.room_schema import RoomCreate


class RoomService:
    def __init__(self, repository):
        self.repository = repository

    def create_room(self, room_data: RoomCreate):
        room = Room(**room_data.dict())
        return self.repository.create(room)

    def get_available_rooms(self, city_id: uuid.UUID, check_in, check_out):
        return self.repository.get_available_rooms(city_id, check_in, check_out)