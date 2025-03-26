import uuid
import re

from exceptions.app_exception import AppException


def validate_request_uuid(id: uuid.UUID):
        if id is None or str(id) == '00000000-0000-0000-0000-000000000000':
            raise AppException("El ID proporcionado no es valido")
        elif not isinstance(id, uuid.UUID):
            raise AppException("El ID proporcionado no es valido")


def validate_empty(text: str, message: str):
        if not text or not text.strip():
            raise AppException(message)


def validate_email(email: str):
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$',email.lower()):
        raise AppException("El correo electrónico no es valido.")