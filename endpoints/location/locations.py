from fastapi import APIRouter, Depends
from domain.utils.dependencies import get_db_context
from models.entities.location.city import City
from models.entities.location.country import Country
from schemas.location.location_schema import CitySchema, CountrySchema
from typing import List

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.get("/cities", response_model=List[CitySchema])
def get_cities(db_context = Depends(get_db_context)):
    with db_context.session() as db:
        cities = db.query(City).all()
        return cities

@router.get("/countries", response_model=List[CountrySchema])
def get_countries(db_context = Depends(get_db_context)):
    with db_context.session() as db:
        countries = db.query(Country).all()
        return countries

