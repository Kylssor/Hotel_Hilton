from models.context.persistence_context import PersistenceContext
from domain.utils.app_context import app_context
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from config import settings


def get_db_context() -> PersistenceContext:
    return app_context.db_context


# Token validator base
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin/employee")  # Puede usarse para ambos

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("id")
        tipo_usuario: str = payload.get("tipo_usuario")
        if user_id is None or tipo_usuario is None:
            raise credentials_exception
        return {"id": user_id, "tipo_usuario": tipo_usuario}
    except JWTError:
        raise credentials_exception


def get_current_employee(user: dict = Depends(get_current_user)) -> dict:
    if user["tipo_usuario"] != "empleado":
        raise HTTPException(status_code=403, detail="Acceso permitido solo a empleados.")
    return user


def get_current_customer(user: dict = Depends(get_current_user)) -> dict:
    if user["tipo_usuario"] != "cliente":
        raise HTTPException(status_code=403, detail="Acceso permitido solo a clientes.")
    return user