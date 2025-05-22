from typing import List
from uuid import UUID
from datetime import date

from fastapi import HTTPException, status

from models.entities.reservation.reservation import Reservation
from models.entities.reservation.reservationstatus import ReservationStatus
from models.repository.unit_of_work import UnitOfWork
from models.repository.generic_repository import GenericRepository
from models.entities.room.room import Room
from models.entities.user.customer import Customer

class ReservationService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.room_repo = GenericRepository(uow.session, Room)
        self.reservation_repo = GenericRepository(uow.session, Reservation)
        self.customer_repo = GenericRepository(uow.session, Customer)
        self.status_repo = GenericRepository(uow.session, ReservationStatus)

    def create_reservation(self, data):
        reservation = Reservation(**data.dict())
        self.reservation_repo.add(reservation)
        return reservation

    def get_customer_reservations(self, customer_id: UUID, upcoming: bool = False, history: bool = False) -> List[Reservation]:
        today = date.today()
        filters = [Reservation.customer_id == customer_id]

        if upcoming:
            filters.append(Reservation.check_in_date >= today)
        elif history:
            filters.append(Reservation.check_in_date < today)

        return self.reservation_repo.read_by_options(
            *filters,
            include_propiertys="room"
        )

    def get_all_reservations(self):
        return self.reservation_repo.read_by_options(
            include_propiertys="room.location"
        )

    def cancel_reservation(self, reservation_id: UUID) -> Reservation:
        reservation = self.reservation_repo.read_by_filter_one(Reservation.id == reservation_id)
        if not reservation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada.")

        status_cancelled = self.status_repo.read_by_filter_one(ReservationStatus.name == "Cancelada")
        if not status_cancelled:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Estado 'Cancelada' no encontrado.")

        reservation.status_id = status_cancelled.id
        return self.reservation_repo.update(reservation)

    def complete_reservation(self, reservation_id: UUID) -> Reservation:
        reservation = self.reservation_repo.read_by_filter_one(Reservation.id == reservation_id)
        if not reservation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada.")

        status_completed = self.status_repo.read_by_filter_one(ReservationStatus.name == "Completada")
        if not status_completed:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Estado 'Completada' no encontrado.")

        reservation.status_id = status_completed.id
        return self.reservation_repo.update(reservation)
