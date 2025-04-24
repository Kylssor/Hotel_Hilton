import uuid
from models.entities.room.room import Location, Room, RoomStatus, RoomType
from models.repository.generic_repository import GenericRepository
from models.repository.unit_of_work import UnitOfWork
from models.entities.location.city import City


def create(uow: UnitOfWork):
    # Asumimos que los RoomStatus y RoomType ya existen
    room_status_repo = GenericRepository(uow.session, RoomStatus)
    room_type_repo = GenericRepository(uow.session, RoomType)
    location_repo = GenericRepository(uow.session, Location)
    room_repo = GenericRepository(uow.session, Room)
    city_repo = GenericRepository(uow.session, City)

    disponible = room_status_repo.read_by_options(RoomStatus.name == "Disponible")
    estandar = room_type_repo.read_by_options(RoomType.name == "Estándar")
    suite = room_type_repo.read_by_options(RoomType.name == "Suite")

    if not (disponible and estandar and suite):
        raise Exception("Asegúrese de que existan RoomStatus 'Disponible' y tipos 'Estándar' y 'Suite'")

    # Obtener ciudades
    medellin = city_repo.read_by_options(City.name == "Medellín")
    bogota = city_repo.read_by_options(City.name == "Bogotá")
    if not (medellin and bogota):
        raise Exception("Debe existir Medellín y Bogotá en ciudades")

    # Crear ubicaciones (hoteles)
    hilton = Location(
        name="Hilton Medellín",
        address="Carrera 43A #1-50, Medellín",
        phone="+57 4 4440000",
        city_id=medellin[0].id
    )
    marriott = Location(
        name="Marriott Bogotá",
        address="Avenida El Dorado #69B-53, Bogotá",
        phone="+57 1 4851111",
        city_id=bogota[0].id
    )

    location_repo.add_all([hilton, marriott])
    uow.session.flush()  # Para obtener los IDs

    # Crear habitaciones con imágenes
    rooms = [
        Room(
            number="101",
            type_id=estandar[0].id,
            status_id=disponible[0].id,
            price_per_night=150.00,
            size=30.0,
            description="Habitación estándar con cama doble",
            tax=10.0,
            image_url="https://example.com/images/room101.jpg",
            location_id=hilton.id
        ),
        Room(
            number="102",
            type_id=suite[0].id,
            status_id=disponible[0].id,
            price_per_night=250.00,
            size=45.0,
            description="Suite con vista al río",
            tax=12.0,
            image_url="https://example.com/images/room102.jpg",
            location_id=hilton.id
        ),
        Room(
            number="201",
            type_id=estandar[0].id,
            status_id=disponible[0].id,
            price_per_night=140.00,
            size=28.0,
            description="Habitación económica",
            tax=9.5,
            image_url="https://example.com/images/room201.jpg",
            location_id=hilton.id
        ),
        Room(
            number="301",
            type_id=suite[0].id,
            status_id=disponible[0].id,
            price_per_night=300.00,
            size=50.0,
            description="Suite ejecutiva",
            tax=13.0,
            image_url="https://example.com/images/room301.jpg",
            location_id=marriott.id
        ),
        Room(
            number="302",
            type_id=estandar[0].id,
            status_id=disponible[0].id,
            price_per_night=160.00,
            size=32.0,
            description="Con cama king y escritorio",
            tax=10.5,
            image_url="https://example.com/images/room302.jpg",
            location_id=marriott.id
        )
    ]

    room_repo.add_all(rooms)
    uow.session.flush()