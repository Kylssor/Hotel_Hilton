from fastapi import APIRouter

from endpoints.users.auth import auth_router
from endpoints.users.users import router as user_router


routers = APIRouter()

router_list = [
    auth_router,
    user_router
]

for router in router_list:
    routers.include_router(router)