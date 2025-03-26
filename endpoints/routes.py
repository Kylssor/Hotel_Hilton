from fastapi import APIRouter

from endpoints.users.auth import auth_router

routers = APIRouter()

router_list = [
    auth_router
]

for router in router_list:
    routers.include_router(router)