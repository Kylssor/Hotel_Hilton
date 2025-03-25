from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from core.dependencies import get_current_user
from core.database import get_db
from schemas.user.user_schema import UserCreateSchema, UserResponseSchema
from models.entities.user.person import Person
from models.entities.user.customer import Customer
from core.security import get_password_hash

router = APIRouter(tags=["Usuarios"])

@router.post("/registro/cliente", response_model=UserResponseSchema)
async def registrar_cliente(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    # Verificar si el email ya existe
    if db.query(Person).filter(Person.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Crear persona
    nueva_persona = Person(
        first_name=user_data.name,
        last_name=user_data.last_name,
        email=user_data.email,
        phone="",
        address=""
    )
    
    # Crear cliente
    nuevo_cliente = Customer(
        person=nueva_persona,
        loyalty_points=0,
        password_hash=get_password_hash(user_data.password)
    )
    
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    
    return nuevo_cliente

@router.get("/perfil", response_model=UserResponseSchema)
async def ver_perfil(usuario_actual: Customer = Depends(get_current_user)):
    return usuario_actual