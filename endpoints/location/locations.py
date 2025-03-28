from fastapi import APIRouter, Depends
from typing import List
from domain.utils.dependencies import get_db_context
from domain.service.location_service import LocationService
from schemas.location.location_schema import CitySchema, CountrySchema

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.get("/cities", response_model=List[CitySchema])
def get_cities(db_context=Depends(get_db_context)):
    with db_context.session() as db:
        service = LocationService(db)
        return service.get_cities()

@router.get("/countries", response_model=List[CountrySchema])
def get_countries(db_context=Depends(get_db_context)):
    with db_context.session() as db:
        service = LocationService(db)
        return service.get_countries()


