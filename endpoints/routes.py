from fastapi import APIRouter

from endpoints.users.auth import auth_router
from endpoints.users.users import router as user_router
from endpoints.reservation.reservations import router as reservation_router
from endpoints.location.locations import router as location_service_router

routers = APIRouter()

router_list = [
    auth_router,
    user_router,
    reservation_router,
    location_service_router
]

for router in router_list:
    routers.include_router(router)