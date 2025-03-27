from passlib.hash import bcrypt
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from config.settings import settings
from exceptions.unauthorized_exception import UnauthorizedException


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


def validate_jwt_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("id")
        if user_id is None:
            raise UnauthorizedException("Token inválido")
        return user_id
    except JWTError:
        raise UnauthorizedException("Token inválido")
