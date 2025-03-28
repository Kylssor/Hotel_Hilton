from models.entities.location.city import City
from models.entities.location.country import Country

class LocationService:
    def __init__(self, db_session):
        self.db = db_session

    def get_cities(self):
        return self.db.query(City).all()

    def get_countries(self):
        return self.db.query(Country).all()