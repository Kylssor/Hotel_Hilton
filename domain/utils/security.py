import hashlib
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext

from config.project_config import ProjectConfig
from exceptions.unauthorized_exception import UnauthorizedException

SECRET_KEY = "tu_clave_secreta_super_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def hash_sha256(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def create_access_jwt_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(hours=24)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, ProjectConfig.SECRET_KEY(), algorithm=ProjectConfig.ALGORITHM())
        return encoded_jwt


def validate_jwt_token(token: str) -> str:
    try:
        payload = jwt.decode(token, ProjectConfig.SECRET_KEY(), algorithms=[ProjectConfig.ALGORITHM()])
        id: str = payload.get("id")
        if id is None:
            raise UnauthorizedException("Token invalido")
    
        return id
    except JWTError:
        raise UnauthorizedException("Token invalido")