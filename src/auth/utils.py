from passlib.context import CryptContext
from datetime import timedelta, datetime
import uuid

import jwt

from src.config import JWT_SECRET, JWT_ALGORITHM
from src.db.redis import is_access_token_blacklisted

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_hashed_password(password: str):
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)


# main function to create tokens

def _create_token(token_type: str, user_data: dict, expiry: timedelta):
    payload = {
        "type": token_type,
        "user": user_data,
        "jti": str(uuid.uuid4()),
        "exp": datetime.utcnow() + expiry,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def create_access_token(user_data: dict, expiry: timedelta):
    return _create_token("access", user_data, expiry)


def create_refresh_token(user_data: dict, expiry: timedelta):
    # Stateless refresh token (JWT only). No DB persistence.
    return _create_token("refresh", user_data, expiry)

def _decode_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.pyjwt.exceptions.ExpiredSignatureError:
        raise Exception("Token has expired")


def decode_access_token(token: str):
    payload = _decode_token(token)
    if payload.get("type") != "access":
        raise Exception("Invalid token type")
    return payload


def decode_refresh_token(token: str):
    payload = _decode_token(token)
    if payload.get("type") != "refresh":
        raise Exception("Invalid token type")
    return payload


