from fastapi import FastAPI
from core.database import engine
from models.entities.base.Base_entity import BaseEntity
from endpoints.users.auth import router as auth_router
from endpoints.users.users import router as users_router

app = FastAPI()

# Crear tablas (solo para desarrollo)
BaseEntity.SQLModel.metadata.create_all(engine)

# Registrar routers
app.include_router(auth_router, prefix="/auth")
app.include_router(users_router, prefix="/usuarios")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)