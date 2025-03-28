import uuid
from models.entities.location.city import City
from models.entities.location.country import Country
from models.repository.generic_repository import GenericRepository
from models.repository.unit_of_work import UnitOfWork

class LocationService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.city_repo = GenericRepository(uow.session, City)
        self.country_repo = GenericRepository(uow.session, Country)


    def get_cities(self, country_id: uuid.UUID):
        return self.city_repo.read_by_options(
            City.country_id == country_id
        )


    def get_countries(self):
        return self.country_repo.read_by_options()