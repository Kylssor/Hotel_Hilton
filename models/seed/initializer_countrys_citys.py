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
        Country(name="Colombia", iso_code="CO"),
        Country(name="Estados Unidos", iso_code="US"),
        Country(name="Argentina", iso_code="AR"),
        Country(name="Reino Unido", iso_code="UK"),
        Country(name="Francia", iso_code="FR"),
        Country(name="Emiratos Árabes", iso_code="AE"),
        Country(name="Japón", iso_code="JP"),
        Country(name="Brasil", iso_code="BR"),
        Country(name="México", iso_code="MX"),
        Country(name="Chile", iso_code="CL"),
        Country(name="Alemania", iso_code="DE"),
        Country(name="España", iso_code="ES"),
        Country(name="Australia", iso_code="AU"),
        Country(name="Etiopía", iso_code="ET"),
        Country(name="Kenia", iso_code="KE"),
        Country(name="Líbano", iso_code="LB"),
        Country(name="Turquía", iso_code="TR"),
        Country(name="Catar", iso_code="QA"),
        Country(name="Baréin", iso_code="BH"),
        Country(name="Malasia", iso_code="MY"),
        Country(name="Singapur", iso_code="SG"),
        Country(name="China", iso_code="CN"),
        Country(name="Austria", iso_code="AT"),
        Country(name="Países Bajos", iso_code="NL"),
        Country(name="Panamá", iso_code="PA"),
        Country(name="Ecuador", iso_code="EC"),
        Country(name="Uruguay", iso_code="UY"),
        Country(name="República Checa", iso_code="CZ"),
        Country(name="Hungría", iso_code="HU"),
        Country(name="Italia", iso_code="IT"),
        Country(name="Malta", iso_code="MT"),
        Country(name="Seychelles", iso_code="SC"),
        Country(name="Egipto", iso_code="EG")
    ]
    country_repo.add_all(countrys)
    uow.session.flush()  
    
    citys = [
        City(name="Bogotá", country_id=countrys[0].id),
        City(name="Cartagena", country_id=countrys[0].id),
        City(name="Santa Marta", country_id=countrys[0].id),
        City(name="Miami", country_id=countrys[1].id),
        City(name="Los Angeles", country_id=countrys[1].id),
        City(name="New York", country_id=countrys[1].id),
        City(name="San Francisco", country_id=countrys[1].id),
        City(name="Orlando", country_id=countrys[1].id),
        City(name="Chicago", country_id=countrys[1].id),
        City(name="Atlanta", country_id=countrys[1].id),
        City(name="San Diego", country_id=countrys[1].id),
        City(name="Waikiki Beach", country_id=countrys[1].id),
        City(name="Buenos Aires", country_id=countrys[2].id),
        City(name="London", country_id=countrys[3].id),
        City(name="Paris", country_id=countrys[4].id),
        City(name="Dubai", country_id=countrys[5].id),
        City(name="Tokyo", country_id=countrys[6].id),
        City(name="Rio de Janeiro", country_id=countrys[7].id),
        City(name="Sao Paulo", country_id=countrys[7].id),
        City(name="Mexico City", country_id=countrys[8].id),
        City(name="Santiago", country_id=countrys[9].id),
        City(name="Munich", country_id=countrys[10].id),
        City(name="Barcelona", country_id=countrys[11].id),
        City(name="Sydney", country_id=countrys[12].id),
        City(name="Addis Ababa", country_id=countrys[13].id),
        City(name="Nairobi", country_id=countrys[14].id),
        City(name="Beirut", country_id=countrys[15].id),
        City(name="Istanbul", country_id=countrys[16].id),
        City(name="Doha", country_id=countrys[17].id),
        City(name="Manama", country_id=countrys[18].id),
        City(name="Kuala Lumpur", country_id=countrys[19].id),
        City(name="Singapore", country_id=countrys[20].id),
        City(name="Beijing", country_id=countrys[21].id),
        City(name="Vienna", country_id=countrys[22].id),
        City(name="Amsterdam", country_id=countrys[23].id),
        City(name="Panama City", country_id=countrys[24].id),
        City(name="Guayaquil", country_id=countrys[25].id),
        City(name="Montevideo", country_id=countrys[26].id),
        City(name="Prague", country_id=countrys[27].id),
        City(name="Budapest", country_id=countrys[28].id),
        City(name="Milan", country_id=countrys[29].id),
        City(name="Malta", country_id=countrys[30].id),
        City(name="Mahé", country_id=countrys[31].id),
        City(name="Cairo", country_id=countrys[32].id)
    ]
    city_repo.add_all(citys)
