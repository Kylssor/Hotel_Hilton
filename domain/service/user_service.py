from exceptions.app_exception import AppException
from domain.utils.list_helper import first_or_none
from models.entities.user.customer import Customer
from models.entities.user.employeed import Employeed
from models.entities.user.person import Person
from models.entities.user.role import Role
from models.repository.generic_repository import GenericRepository
from models.repository.unit_of_work import UnitOfWork
from schemas.user.user_schemas import EmployeedCreateSchema, EmployeedResponseSchema, UserCreateSchema, UserResponseSchema
from domain.utils.security import get_password_hash


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.person_repo = GenericRepository(uow.session, Person)
        self.employeed_repo = GenericRepository(uow.session, Employeed)
        self.customer_repo = GenericRepository(uow.session, Customer)
        self.role_repo = GenericRepository(uow.session, Role)


    def register_customer(self, user_data: UserCreateSchema):
        existing_acount = first_or_none(self.person_repo.delete_by_options(
            Person.email == user_data.email
        ))

        if existing_acount:
            raise AppException("Ya existe una cuenta registrada con este correo.")

        new_person = Person(
            identification_number=user_data.identification_number,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            phone=user_data.phone,
            address=user_data.address,
            city_id=user_data.city_id
        )
        
        person = self.__get_person(user_data.identification_number)
        
        if person:
            customer = self.customer_repo.read_by_options(
                Customer.person_id == person.id
            )
            
            if customer:
                raise AppException("Ya existe una cuenta registrada con tus datos")
            
            new_person.id = person.id
            self.person_repo.update(new_person)
        else:
            self.person_repo.add(new_person)

        self.customer_repo.add(Customer(
            person_id=new_person.id,
            password_hash=get_password_hash(user_data.password)
        ))


    def register_employee(self, user_data: EmployeedCreateSchema):
        person = self.__get_person(user_data.identification_number)

        new_person = Person(
            identification_number=user_data.identification_number,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            phone=user_data.phone,
            address=user_data.address,
            city_id=user_data.city_id
        )
        
        if person:
            existing_acount = self.employeed_repo.read_by_options(
                Employeed.person_id == person.id
            )

            if existing_acount:
                raise AppException("Este empleado ya esta registrado")
            
            new_person.id = person.id
            self.person_repo.update(new_person)
        else:
            self.person_repo.add(new_person)


        new_employeed = Employeed(
            person_id=new_person.id,
            role_id=user_data.role_id,
            user_name= self.__generate_unique_username(
                user_data.first_name,
                user_data.last_name
            ),
            password_hash=get_password_hash(user_data.password)
        )
        self.employeed_repo.add(new_employeed)
        
        return new_employeed.user_name



    def get_customer_profile(self, usuario)-> UserResponseSchema:
        customer: Customer = self.customer_repo.read_by_id(
            usuario["id"],
            include_propiertys="persons"
        )
        return UserResponseSchema(
            id=customer.id,
            identification_number=customer.persons.identification_number,
            first_name=customer.persons.first_name,
            last_name=customer.persons.last_name,
            email=customer.persons.email,
            phone=customer.persons.phone,
            address=customer.persons.address,
            country=customer.persons.city.country.name,
            city=customer.persons.city.name
        )

    def get_employee_profile(self, usuario)-> EmployeedResponseSchema:
        employeed: Employeed = self.employeed_repo.read_by_id(
            usuario["id"],
            include_propiertys="roles,persons"
        )
        return EmployeedResponseSchema(
            id=employeed.id,
            identification_number=employeed.persons.identification_number,
            first_name=employeed.persons.first_name,
            last_name=employeed.persons.last_name,
            user_name=employeed.user_name,
            email=employeed.persons.email,
            phone=employeed.persons.phone,
            address=employeed.persons.address,
            country=employeed.persons.city.country.name,
            city=employeed.persons.city.name,
            role=employeed.roles.name
        )


    def get_employee_roles(self):
        return self.role_repo.read_by_options()


    def __get_person(self, identification_number: str) -> Person:
        existing_person = first_or_none(self.person_repo.read_by_options(
            Person.identification_number == identification_number
        ))
        
        return existing_person


    def __generate_unique_username(self, first_name: str, last_name: str) -> str:
        base_username = f"{first_name.split()[0].lower()}.{last_name.split()[0].lower()}"
        index = 0

        while True:
            username = f"{base_username}{index if index > 0 else ''}"
            existing = self.employeed_repo.read_by_options(
                Employeed.user_name == username
            )
            
            if not existing:
                return username

            index += 1