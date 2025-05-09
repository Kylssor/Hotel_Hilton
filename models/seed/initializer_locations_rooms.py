from domain.utils.list_helper import first_or_none
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

    disponible = first_or_none(room_status_repo.read_by_options(RoomStatus.name == "Disponible"))
    estandar = first_or_none(room_type_repo.read_by_options(RoomType.name == "Estándar"))
    suite = first_or_none(room_type_repo.read_by_options(RoomType.name == "Suite"))

    if not (disponible and estandar and suite):
        raise Exception("Asegúrese de que existan RoomStatus 'Disponible' y tipos 'Estándar' y 'Suite'")

    # Obtener ciudades
    medellin = first_or_none(city_repo.read_by_options(City.name == "Medellín"))

    bogota = first_or_none(city_repo.read_by_options(City.name == "Bogotá"))

    if not (medellin and bogota):
        raise Exception("Debe existir Medellín y Bogotá en ciudades")

    # Verificar ubicaciones (hoteles)
    hilton = first_or_none(location_repo.read_by_options(Location.name == "Hilton Medellín"))
    if not hilton:
        hilton = Location(
            name="Hilton Medellín",
            address="Carrera 43A #1-50, Medellín",
            phone="+57 4 4440000",
            city_id=medellin.id
        )
        location_repo.add(hilton)

    marriott = first_or_none(location_repo.read_by_options(Location.name == "Marriott Bogotá"))
    if not marriott:
        marriott = Location(
            name="Marriott Bogotá",
            address="Avenida El Dorado #69B-53, Bogotá",
            phone="+57 1 4851111",
            city_id=bogota.id
        )
        location_repo.add(marriott)

    # Rooms por location
    rooms_data = [
        {"number": "101", "type": estandar, "location": hilton, "price": 150.00, "size": 30.0, "desc": "Habitación estándar con cama doble", "tax": 10.0, "image": "https://example.com/images/room101.jpg"},
        {"number": "102", "type": suite, "location": hilton, "price": 250.00, "size": 45.0, "desc": "Suite con vista al río", "tax": 12.0, "image": "https://example.com/images/room102.jpg"},
        {"number": "201", "type": estandar, "location": hilton, "price": 140.00, "size": 28.0, "desc": "Habitación económica", "tax": 9.5, "image": "https://example.com/images/room201.jpg"},
        {"number": "301", "type": suite, "location": marriott, "price": 300.00, "size": 50.0, "desc": "Suite ejecutiva", "tax": 13.0, "image": "https://example.com/images/room301.jpg"},
        {"number": "302", "type": estandar, "location": marriott, "price": 160.00, "size": 32.0, "desc": "Con cama king y escritorio", "tax": 10.5, "image": "https://example.com/images/room302.jpg"}
    ]

    for data in rooms_data:
        existing_room_list = room_repo.read_by_options(
            (Room.number == data["number"]) & (Room.location_id == data["location"].id)
        )
        if not existing_room_list:
            new_room = Room(
                number=data["number"],
                type_id=data["type"].id,
                status_id=disponible.id,
                price_per_night=data["price"],
                size=data["size"],
                description=data["desc"],
                tax=data["tax"],
                image_url=data["image"],
                location_id=data["location"].id
            )
            room_repo.add(new_room)