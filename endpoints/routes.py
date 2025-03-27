from fastapi import APIRouter

from endpoints.users.auth import auth_router
from endpoints.users.users import router as user_router
from endpoints.location.locations import router as location_router


routers = APIRouter()

router_list = [
    auth_router,
    user_router,
    location_router
]

for router in router_list:
    routers.include_router(router)