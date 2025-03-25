from fastapi import APIRouter

from endpoints.users.auth import router as auth_router
from endpoints.users.users import router as users_router

# Crea el router principal
routers = APIRouter()

# Lista de routers a incluir
router_list = [
    auth_router,
    users_router
    

]

# Incluye todos los routers en el principal
for router in router_list:
    routers.include_router(router)