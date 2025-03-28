# routers/users.py
from fastapi import APIRouter, Depends
from domain.utils.dependencies import get_current_employee, get_current_customer
from domain.service.user_service import UserService

router = APIRouter(prefix="/user", tags=["Users"])
user_service = UserService()

@router.get("/cliente/perfil")
async def perfil_cliente(usuario=Depends(get_current_customer)):
    return user_service.get_cliente_profile(usuario)

@router.get("/empleado/perfil")
async def perfil_empleado(usuario=Depends(get_current_employee)):
    return user_service.get_empleado_profile(usuario)

