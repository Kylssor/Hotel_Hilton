from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from models.entities.user.person import Person
from schemas.authentication.sign_in_schema import SignInSchema
from schemas.authentication.token_schema import TokenSchema
from models.entities.user.employeed import Employeed
from models.entities.user.customer import Customer
from core.database import get_db
from core.security import verify_password, create_access_token

router = APIRouter(tags=["Autenticación"])

async def authenticate_user(email: str, password: str, db: Session, is_employee: bool = False):
    # Buscar en empleados o clientes según el caso
    if is_employee:
        user = db.query(Employeed).join(Person).filter(Person.email == email).first()
    else:
        user = db.query(Customer).join(Person).filter(Person.email == email).first()
    
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

@router.post("/login/cliente", response_model=TokenSchema)
async def login_cliente(form_data: SignInSchema, db: Session = Depends(get_db)):
    user = await authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return {
        "access_token": create_access_token({"sub": str(user.id), "role": "cliente"}),
        "token_type": "bearer"
    }

@router.post("/login/empleado", response_model=TokenSchema)
async def login_empleado(form_data: SignInSchema, db: Session = Depends(get_db)):
    user = await authenticate_user(form_data.email, form_data.password, db, is_employee=True)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return {
        "access_token": create_access_token({"sub": str(user.id), "role": "empleado"}),
        "token_type": "bearer"
    }