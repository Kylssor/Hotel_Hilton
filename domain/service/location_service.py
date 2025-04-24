from typing import List
from uuid import UUID
from datetime import date
from fastapi import HTTPException

from models.entities.location.location import Location
from models.entities.room.roomstatus import RoomStatus
from models.repository.generic_repository import GenericRepository
from models.repository.unit_of_work import UnitOfWork
from models.entities.room.room import Room
from models.entities.location.city import City
from models.entities.location.country import Country

class LocationService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.location_repo = GenericRepository(uow.session, Location)
        self.room_repo = GenericRepository(uow.session, Room)
        self.status_repo = GenericRepository(uow.session, RoomStatus)
        self.city_repo = GenericRepository(uow.session, City)
        self.country_repo = GenericRepository(uow.session, Country)

    def get_available_locations(self, check_in: date, check_out: date) -> List[Location]:
        status = self.status_repo.read_by_options(RoomStatus.name == "Disponible")
        if not status:
            raise HTTPException(status_code=400, detail="Estado 'Disponible' no encontrado")

        status_id = status[0].id
        all_locations = self.location_repo.read_by_options()

        available_locations = []
        for loc in all_locations:
            has_room = self.uow.session.query(Room).filter(
                Room.location_id == loc.id,
                Room.status_id == status_id
            ).first()
            if has_room:
                available_locations.append(loc)

        return available_locations

    def get_rooms_by_location(self, location_id: UUID) -> List[Room]:
        status = self.status_repo.read_by_options(RoomStatus.name == "Disponible")
        if not status:
            raise HTTPException(status_code=400, detail="Estado 'Disponible' no existe")

        return self.room_repo.read_by_options(
            Room.location_id == location_id,
            Room.status_id == status[0].id
        )

    def get_room_detail(self, room_id: UUID) -> Room:
        room = self.room_repo.read_by_id(room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Habitación no encontrada")
        return room

    def list_all_locations(self) -> List[Location]:
        return self.location_repo.read_by_options()

    def list_all_rooms(self) -> List[Room]:
        return self.room_repo.read_by_options(include_propiertys="status")

    def get_cities_by_country(self, country_id: UUID) -> List[City]:
        return self.city_repo.read_by_options(City.country_id == country_id)

    def get_all_countries(self) -> List[Country]:
        return self.country_repo.read_by_options()