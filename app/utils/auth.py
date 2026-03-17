import bcrypt
import jwt
from datetime import datetime, timedelta
from app.core.config import settings

secret_auth_key = settings.secret_auth_key
algorithm = settings.algorithm
access_token_expires_minutes = settings.access_token_expires_minutes


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=access_token_expires_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_auth_key, algorithm=algorithm)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, secret_auth_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except jwt.PyJWTError:
        return None
