from fastapi import APIRouter, Depends
from domain.utils.dependencies import get_current_employee, get_current_customer

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.get("/cliente/perfil")
async def perfil_cliente(usuario=Depends(get_current_customer)):
    return {
        "message": "Bienvenido cliente",
        "usuario_id": usuario["id"]
    }

@router.get("/empleado/perfil")
async def perfil_empleado(usuario=Depends(get_current_employee)):
    return {
        "message": "Bienvenido empleado",
        "usuario_id": usuario["id"]
    }
