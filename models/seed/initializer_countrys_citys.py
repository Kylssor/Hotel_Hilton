from models.entities.location.city import City
from models.entities.location.country import Country
from models.repository.generic_repository import GenericRepository
from models.repository.unit_of_work import UnitOfWork


def create(uow: UnitOfWork):
    country_repo = GenericRepository(uow.session, Country)
    city_repo = GenericRepository(uow.session, City)

    count: int = len(country_repo.read_by_options())

    if count != 0:
        return
    
    countrys = [
        Country(
            name="Colombia",
            iso_code="CO"
        ),
        Country(
            name="Estados Unidos",
            iso_code="US"
        ),
    ]
    country_repo.add_all(countrys)

    citys = [
        City(
            name="Bogota D.C.",
            country_id=countrys[0].id
        ),
        City(
            name="Miami",
            country_id=countrys[1].id
        )
    ]
    city_repo.add_all(citys)