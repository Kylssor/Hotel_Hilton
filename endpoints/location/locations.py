from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List
from uuid import UUID
from datetime import date

from domain.utils.dependencies import get_db_context
from domain.service.location_service import LocationService
from models.context.persistence_context import PersistenceContext
from schemas.location.location_schema import LocationRead, CitySchema, CountrySchema
from models.repository.unit_of_work import UnitOfWork
from schemas.room.room_schema import RoomRead

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.get("/available", response_model=List[LocationRead])
def get_available_locations(
    check_in: date = Query(...),
    check_out: date = Query(...),
    db_context: PersistenceContext = Depends(get_db_context)
):
    uow = UnitOfWork(db_context)
    service = LocationService(uow)
    return service.get_available_locations(check_in, check_out)


@router.get("/{location_id}/rooms", response_model=List[RoomRead])
def get_available_rooms_by_location(
    location_id: UUID,
    db_context: PersistenceContext = Depends(get_db_context)
):
    uow = UnitOfWork(db_context)
    service = LocationService(uow)
    return service.get_rooms_by_location(location_id)


@router.get("/room/{room_id}", response_model=RoomRead)
def get_room_detail(
    room_id: UUID,
    db_context: PersistenceContext = Depends(get_db_context)
):
    uow = UnitOfWork(db_context)
    service = LocationService(uow)
    return service.get_room_detail(room_id)


@router.get("/all", response_model=List[LocationRead])
def list_all_locations(
    db_context: PersistenceContext = Depends(get_db_context)
):
    uow = UnitOfWork(db_context)
    service = LocationService(uow)
    return service.list_all_locations()


@router.get("/rooms", response_model=List[RoomRead])
def list_all_rooms(
    db_context: PersistenceContext = Depends(get_db_context)
):
    uow = UnitOfWork(db_context)
    service = LocationService(uow)
    return service.list_all_rooms()


@router.get("/cities/{country_id}", response_model=List[CitySchema])
def get_cities_by_country(
    country_id: UUID,
    db_context: PersistenceContext = Depends(get_db_context)
):
    uow = UnitOfWork(db_context)
    service = LocationService(uow)
    return service.get_cities_by_country(country_id)


@router.get("/countries", response_model=List[CountrySchema])
def get_all_countries(
    db_context: PersistenceContext = Depends(get_db_context)
):
    uow = UnitOfWork(db_context)
    service = LocationService(uow)
    return service.get_all_countries()
