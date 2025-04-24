from dotenv import load_dotenv
from domain.utils.security import get_password_hash, hash_sha256
from models.entities.location.city import City
from models.entities.user.employeed import Employeed
from models.entities.user.person import Person
from models.entities.user.role import Role
from models.repository.generic_repository import GenericRepository
from models.repository.unit_of_work import UnitOfWork
import os

load_dotenv()

def create(uow: UnitOfWork):
    person_repo = GenericRepository(uow.session, Person)
    employeed_repo = GenericRepository(uow.session, Employeed)

    if employeed_repo.read_by_options():
        return

    city_repo = GenericRepository(uow.session, City)
    role_repo = GenericRepository(uow.session, Role)

    city = city_repo.read_by_options(City.name == "Bogotá")
    role = role_repo.read_by_options(Role.name == "SuperAdmin")

    person = Person(
        identification_number="1007727136",
        first_name="Gustavo Andres",
        last_name="Romero Ordoñez",
        email="gus.romero.orondez@outlook.com",
        phone="3151234567",
        address="Calle 123 # 456 - 789",
        city_id=city[0].id
    )

    employeed = Employeed(
        person_id=person.id,
        role_id=role[0].id,
        user_name="gustavo.romero",
        password_hash=get_password_hash(hash_sha256(os.getenv("SUPER_ADMIN_PASS")))
    )

    person_repo.add(person)
    employeed_repo.add(employeed)