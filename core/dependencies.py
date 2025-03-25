from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session
from core.security import verify_password, create_access_token
from core.database import get_db
from core.config import settings
from models.entities.user.customer import Customer
from models.entities.user.employeed import Employeed

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/cliente")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    if role == "cliente":
        user = db.query(Customer).filter(Customer.id == user_id).first()
    elif role == "empleado":
        user = db.query(Employeed).filter(Employeed.id == user_id).first()
    else:
        raise credentials_exception
    
    if not user:
        raise credentials_exception
    return user