import uuid
from fastapi import APIRouter, Depends
from typing import List
from domain.utils.dependencies import get_db_context
from domain.service.location_service import LocationService
from models.repository.unit_of_work import UnitOfWork
from schemas.location.location_schema import CitySchema, CountrySchema

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.get("/cities/{country_id}", response_model=List[CitySchema])
def get_cities(country_id: uuid.UUID, db=Depends(get_db_context)):
    uow = UnitOfWork(db)
    service = LocationService(uow)
    return service.get_cities(country_id)


@router.get("/countries", response_model=List[CountrySchema])
def get_countries(db=Depends(get_db_context)):
    uow = UnitOfWork(db)
    service = LocationService(uow)
    return service.get_countries()


