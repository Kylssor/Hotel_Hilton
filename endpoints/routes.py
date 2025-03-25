from fastapi import APIRouter

from endpoints.users.auth import router as auth_router
from endpoints.users.users import router as users_router

routers = APIRouter()

router_list = [
    auth_router,
    users_router
]

for router in router_list:
    routers.include_router(router)