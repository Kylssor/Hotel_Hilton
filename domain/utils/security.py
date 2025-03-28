import hashlib
from passlib.hash import bcrypt
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from config.settings import settings
from exceptions.unauthorized_exception import UnauthorizedException


def hash_sha256(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def get_password_hash(password: str) -> str:
    return bcrypt.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)


def create_access_jwt_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def validate_token_customer(token: str) -> dict:
    user = __validate_token(token)
    if user["tipo_usuario"] != "cliente":
        raise UnauthorizedException("Acceso no autorizado")
    
    return user


def validate_token_employee(token: str) -> dict:
    user = __validate_token(token)
    if user["tipo_usuario"] != "empleado":
        raise UnauthorizedException("Acceso no autorizado")
    
    return user


def __validate_token(token: str) -> dict:
        credentials_exception = UnauthorizedException("No se pudo validar el token.")
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id: str = payload.get("id")
            tipo_usuario: str = payload.get("tipo_usuario")

            if not user_id or not tipo_usuario:
                raise credentials_exception
            return {"id": user_id, "tipo_usuario": tipo_usuario}
        except JWTError:
            raise credentials_exception

